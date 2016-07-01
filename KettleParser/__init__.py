import os
import xml.etree.ElementTree as ET

__author__ = 'jeffportwood'


class KettleParserError(Exception):
    pass


class KettleNode(object):

    def __init__(self, element):
        self._xml_element = element


    def get_attribute(self, attribute):
        """
        Get attribute from step
        :param attributes: str, name of step attribute
        """
        try:
            return self._xml_element.find(attribute).text
        except AttributeError:
            raise KettleParserError("Unable to find attribute {}".format(attribute))


class Parse(object):
    """
    Parses kettle .ktr and .kjb files for easy manipulation by other tools

    File Types
        1: Transformation
        2: Job
    """
    # Acceptable file endings
    _FILE_ENDINGS = [".ktr", ".kjb"]
    # Elements to extract from step xml
    _STEPITEMS = ["name", "type"]
    # Hop elements
    _ENABLED = {"Y": True, "N": False}

    def __init__(self, kettle_file):

        # Default class parameters
        self.file_type = None
        self.name = ""
        self.steps = []
        self.hops = []
        self.error_hops = []
        self.connections = []
        self.graph = {}

        # Verify and parse file
        self._verify_file(kettle_file)
        self._parse_xml(kettle_file)


    def _verify_file(self, data):
        """
        Verify file ending is acceptable
        """
        if not os.path.isfile(data):
            raise KettleParserError("{} does not exist".format(data))
        if os.path.splitext(data)[1] not in self._FILE_ENDINGS:
            raise KettleParserError("Invalid Kettle file")


    def _parse_xml(self, data):
        """
        Coordinates parsing of XML to its component pieces.
        Will look at XML and determine the following:
            - file_type: "transformation" or "job"
            - name: name of transformation or job

        Also calls parse_steps/parse_hops to get step/hop information
        """
        # Parse xml file
        try:
            xml_root = ET.parse(data).getroot()
        except ET.ParseError:
            raise KettleParserError("Could not parse XML")

        # Determine type of kettle file
        if xml_root.tag == "transformation":
            self.file_type = 1
            self.name = xml_root.find("./info/name").text
        elif xml_root.tag == "job":
            self.file_type = 2
            self.name = xml_root.find("./name").text
        else:
            raise KettleParserError("Invalid Kettle file")

        # Call helper methods
        self._parse_steps(xml_root)
        self._parse_hops(xml_root)
        self._parse_connections(xml_root)
        self._parse_error_handling(xml_root)


    def _parse_steps(self, xml_root):
        """
        Build list of step objects
        """
        if self.file_type == 1:
            step_path = "step"
        elif self.file_type == 2:
            step_path = "./entries/entry"
        for step_elem in xml_root.findall(step_path):
            self.steps.append(KettleNode(step_elem))


    def _parse_hops(self, xml_root):
        """
        Build list of hop objects
        """
        if self.file_type == 1:
            hop_path = "./order"
        elif self.file_type == 2:
            hop_path = "./hops"
        for hop_elem in xml_root.find(hop_path):
            self.hops.append(KettleNode(hop_elem))


    def _parse_connections(self, xml_root):
        """
        Build list of connection objects
        """
        for connection_elem in xml_root.findall("connection"):
            connection = KettleNode(connection_elem)
            self.connections.append(connection)


    def _parse_error_handling(self, xml_root):
        """
        Build list of error handling objects
        """
        for error_elem in xml_root.findall("./step_error_handling/error"):
            self.error_hops.append(KettleNode(error_elem))


    def get_enabled_hops(self):
        return [hop for hop in self.hops if hop.get_attribute("enabled")]


    def get_disabled_hops(self):
        return [hop for hop in self.hops if not hop.get_attribute("enabled")]


    def get_enabled_steps(self):
        enabled_from = []
        enabled_to = []
        for hop in self.get_enabled_hops():
            enabled_from.append(hop.get_attribute("from"))
            enabled_to.append(hop.get_attribute("to"))
        enabled_names = list(set(enabled_from + enabled_to))
        return [step for step in self.steps if step.get_attribute("name") in enabled_names]


    def get_disabled_steps(self):
        disabled_from = []
        disabled_to = []
        for hop in self.get_disabled_hops():
            disabled_from.append(hop.get_attribute("from"))
            disabled_to.append(hop.get_attribute("to"))
        disabled_names = list(set(disabled_from + disabled_to))
        return [step for step in self.steps if step.get_attribute("name") in disabled_names]


    def get_error_hops(self):
        error_hops = []
        for hop in self.hops:
            for error_hop in self.error_hops:
                source = error_hop.get_attribute("source_step")
                target = error_hop.get_attribute("target_step")
                if source == hop.get_attribute("from") and target == hop.get_attribute("to"):
                    error_hops.append(hop)
        return error_hops


class KettleGraph(object):
    def __init__(self, hops):
        """
        :param hops: list of hop objects
        :param only_enabled:
        """
        self.graph = {}

        self._build_graph(hops)


    def _build_graph(self, hops):
        assert isinstance(hops, list)
        for hop in hops:
            if hop.get_attribute("from") not in self.graph:
                self.graph[hop.get_attribute("from")] = [hop.get_attribute("to")]
            else:
                self.graph[hop.get_attribute("from")].append(hop.get_attribute("to"))


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
