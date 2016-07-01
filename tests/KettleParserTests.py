import copy
import unittest
import KettleParser
import constants

__author__ = 'jeffportwood'

class KettleParserTests(unittest.TestCase):


    def test_parse_xml_file(self):
        trans = KettleParser.Parse(constants.TRANSFORMATION_1_FILE)

        # Steps
        step_dict = {}
        for step in trans.steps:
            step_dict[step.get_attribute("name")] = {"type": step.get_attribute("type")}
        self.assertDictEqual(step_dict, constants.TRANSFORMATION_1_STEPS, "Error parsing steps")

        # Step attributes
        test_steps = copy.deepcopy(constants.TRANSFORMATION_1_STEPS)
        test_steps["Text file input"]["format"] = "Unix"
        for step in trans.steps:
            if step.get_attribute("name") == "Text file input":
                step_dict["Text file input"]["format"] = step.get_attribute("format")
        self.assertDictEqual(step_dict, test_steps, "Error parsing steps")

        # Hops
        hop_list = []
        for hop in trans.hops:
            hop_list.append({"to": hop.get_attribute("to"),
                             'from': hop.get_attribute("from"),
                             'enabled': hop.get_attribute("enabled")})
        self.assertListEqual(hop_list, constants.TRANSFORMATION_1_HOPS, "Error parsing hops")


    def test_kettle_graph(self):
        trans = KettleParser.Parse(constants.TRANSFORMATION_1_FILE)
        kettle_graph = KettleParser.KettleGraph(trans.hops)

        # Graph
        self.assertDictEqual(kettle_graph.graph, constants.TRANSFORMATION_1_GRAPH, "Error parsing graph")

        # Paths
        paths = [path for path in kettle_graph.find_all_paths("Text file input", "Text file output")]
        self.assertListEqual(paths, constants.TRANSFORMATION_1_PATHS)


if __name__ == "__main__":
    unittest.main()
