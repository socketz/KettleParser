import xml.etree.ElementTree as ET
from itertools import permutations

__author__ = 'jeffportwood'


class KettleException(Exception):
    pass


class ParseKettleXml(object):
    """
    Parses kettle .ktr and .kjb files for easy manipulation by other tools
    """
    # Acceptable file endings
    _FILE_ENDINGS = [".ktr", ".kjb"]
    # Elements to extract from step xml
    _STEPITEMS = ["name", "type"]
    # Hop elements
    _HOP_ENABLED = {"Y": True, "N": False}
    _ERROR_ENABLED = {"N": True, "Y": False}

    def __init__(self, data, is_file=True):
        """
        Create object for kettle parsing.
        :param data: str, File pointer or string of kettle XML
        :param is_file: bool, Whether or not data param is a file pointer
        """
        self.data = data
        self.is_file = is_file

        # Default class parameters
        self.file_type = ""
        self.root = None
        self.steps = {}
        self.steps_xml = {}
        self.hops = []
        self.perms = []
        self.error_handling = []
        self.name = ""
        self.step_node = ""
        self.graph = {}
        self.connections = []

        # Parse file to extract metadata
        if self.is_file:
            self.verify_file_type()
        self._parse_xml()


    def verify_file_type(self):
        """
        Verify file ending is acceptable
        """
        if self.data[-4:] not in self._FILE_ENDINGS:
            raise KettleException("Invalid Kettle file")


    def _parse_xml(self):
        """
        Coordinates parsing of XML to its component pieces.
        Will look at XML and determine the following:
            - file_type: "transformation" or "job"
            - name: name of transformation or job

        Also calls parse_steps/parse_hops to get step/hop information
        """
        try:
            if self.is_file:
                self.root = ET.parse(self.data).getroot()
            else:
                self.root = ET.fromstring(self.data)
        except:
            raise KettleException("Could not parse XML")

        if self.root.tag == "transformation":
            self.file_type = "transformation"
            self.name = self._get_text(self.root, "./info/name")
            self.step_node = "step"

        elif self.root.tag == "job":
            self.file_type = "job"
            self.name = self._get_text(self.root, "./name")
            self.step_node = "entry"

        self._parse_steps()
        self._parse_hops()
        self._parse_connections()
        self._build_graph()
        self.build_permutations(length=2)


    def _parse_steps(self):
        """
        Build dictionary of steps key="name", value="type", since name is always
        going to be unique
        """
        # Loop through all steps
        try:
            for step in self.root.iter(self.step_node):
                try:
                    self.steps[self._get_text(step, "name")] = {"type": self._get_text(step, "type")}
                    self.steps_xml[self._get_text(step, "name")] = step
                except AttributeError, e:
                    # no "text" typically means a nested step element, so let's ignore for now
                    continue
        except AttributeError, e:
            raise KettleException(e.message)


    def _parse_hops(self):
        """
        Parse hop metadata and construct hop property ("step_name_from", "step_name_to", "enabled")
            step_name_from: str, name of step that hop originates from
            step_name_to: str, name of step that hop ends at
            enabled: bool, is hop enabled?
            ex: (Sort rows, Group by, True)
        """
        if self.file_type == "transformation":
            self._parse_error_handling_trans()
        # Loop through all hops
        try:
            for hop in self.root.iter("hop"):
                _is_enabled = self._HOP_ENABLED[self._get_text(hop, "enabled")]
                _step_from = self._get_text(hop, "from")
                _step_to = self._get_text(hop, "to")

                # Check for error handling
                _is_error = False
                if self.file_type == "transformation":
                    for error in self.error_handling:
                        if error["from"] == _step_from and error["to"] == _step_to:
                            _is_error = True
                else:
                    _is_error = self._ERROR_ENABLED[self._get_text(hop, "evaluation")]


                self.hops.append({"from": _step_from,
                                  "to": _step_to,
                                  "enabled": _is_enabled,
                                  "error": _is_error})
        except AttributeError, e:
            raise KettleException(e.message)


    def _parse_connections(self):
        """
        Get list of connection XML element objects. Specify certain access type if desired to narrow results.
        :return: list, connection XML elements
        """
        if self.is_file:
            self.root = ET.parse(self.data).getroot()
        else:
            self.root = ET.fromstring(self.data)

        if self.file_type == "transformation":
            for connection in self.root.iter("connection"):
                try:
                    conn = {"name": self._get_text(connection, "name"),
                            "server": self._get_text(connection, "server"),
                            "type": self._get_text(connection, "type"),
                            "access": self._get_text(connection, "access"),
                            "database": self._get_text(connection, "database"),
                            "username": self._get_text(connection, "username")}
                except AttributeError:
                    pass
            self.connections.append(conn)


    def _parse_error_handling_trans(self):
        try:
            for error_handle in self.root.iter("error"):
                try:
                    self.error_handling.append({"from": self.steps[self._get_text(error_handle, "source_step")],
                                                "to": self.steps[self._get_text(error_handle, "target_step")],
                                                "enabled": self._HOP_ENABLED[
                                                    self._get_text(error_handle, "is_enabled")]})
                except KeyError:
                    continue
        except AttributeError, e:
            raise KettleException(e.message)


    def _build_graph(self):
        """
        Only include hops that are enabled.
        :return:
        """
        for hop in self.hops:
            if not hop["enabled"]:
                continue
            if hop["from"] not in self.graph:
                self.graph[hop["from"]] = [hop["to"]]
            else:
                self.graph[hop["from"]].append(hop["to"])
        return self.graph


    def _get_text(self, element, path):
        """
        Return text from XML element
        :param element: xml element object to search in
        :param path: str, tag name or path
        :return: step_type: str
        """
        return element.find(path).text


    def _name_type_lookup(self, step_name):
        """
        This method allows us to get the step type from the step name. This is needed
        because hop metadata in XML only stores step name and not step type.
        :param step_name: str
        :return: step_type: str
        """
        return self.steps.get(step_name)["type"]


    def get_step_attribute(self, step_name, attribute):
        """
        Given an xml element, parse out given attributes text values
        :param element: single step xml element
        :param attributes: list of attributes to parse from xml
        :return: dictionary of attributes and values
        """
        try:
            self.steps[step_name][attribute] = self.steps_xml[step_name].find(attribute).text
        except AttributeError, e:
            raise KettleException("Invalid attribute {} for step {}".format(attribute, step_name))
        return self.steps[step_name][attribute]


    def find_all_paths(self, start, end, path=None):
        """
        Recursive DFS algorithm to find all possible paths between start and end node. Using a
        generator allows the user to only compute the desired amount of paths.
        Adapted from: http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
        :param start: str, start node
        :param end: str, end node
        :return: list, all possible paths
        """
        if path is None:
            path = [start]
        if start == end:
            yield path
        next_items = [item for item in self.graph.get(start, []) if item not in set(path)]
        for next in next_items:
            for sub in self.find_all_paths(next, end, path + [next]):
                yield sub


    def build_permutations(self, length=2):
        """
        Build step permutations for all steps
        :param length: length of each permutation
        :return:
        """
        types = [meta["type"] for step, meta in self.steps.iteritems()]
        self.perms = [tuple(pair) for pair in permutations(types, length)]


    def get_enabled_hops(self):
        return [hop for hop in self.hops if hop["enabled"]]


    def get_disabled_hops(self):
        return [hop for hop in self.hops if not hop["enabled"]]


    def get_enabled_steps(self):
        enabled_hops = self.get_enabled_hops()
        enabled_from = []
        enabled_to = []
        for step in enabled_hops:
            enabled_from.append(step["from"])
            enabled_to.append(step["to"])
        enabled_names = list(set(enabled_from + enabled_to))
        return {step: meta for step, meta in self.steps.iteritems() if step in enabled_names}


    def get_disabled_steps(self):
        disabled_hops = self.get_disabled_hops()
        disabled_from = []
        disabled_to = []
        for step in disabled_hops:
            disabled_from.append(step["from"])
            disabled_to.append(step["to"])
        disabled_names = list(set(disabled_from + disabled_to))
        return {step: meta for step, meta in self.steps.iteritems() if step in disabled_names}
