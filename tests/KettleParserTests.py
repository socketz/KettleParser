import copy
import unittest
import KettleParser
import constants

__author__ = 'jeffportwood'

class KettleParserTests(unittest.TestCase):

    def test_parse_xml_file(self):
        trans = KettleParser.ParseKettleXml(constants.TRANSFORMATION_1_FILE)

        # Steps
        self.assertDictEqual(trans.steps, constants.TRANSFORMATION_1_STEPS, "Error parsing steps")

        # Step attributes
        test_steps = copy.deepcopy(constants.TRANSFORMATION_1_STEPS)
        test_steps["Text file input"]["format"] = "Unix"
        trans.get_step_attribute("Text file input", "format")
        self.assertDictEqual(trans.steps, test_steps, "Error parsing steps")

        # Hops
        self.assertListEqual(trans.hops, constants.TRANSFORMATION_1_HOPS, "Error parsing hops")

        # Graph
        self.assertDictEqual(trans.graph, constants.TRANSFORMATION_1_GRAPH, "Error parsing graph")

        # Paths
        paths = [path for path in trans.find_all_paths("Text file input", "Text file output")]
        self.assertListEqual(paths, constants.TRANSFORMATION_1_PATHS)


    def test_parse_xml_raw(self):
        trans = KettleParser.ParseKettleXml(constants.TRANSFORMATION_1_XML.strip(), is_file=False)

        # Steps
        self.assertDictEqual(trans.steps, constants.TRANSFORMATION_1_STEPS, "Error parsing steps")

        # Step attributes
        test_steps = copy.deepcopy(constants.TRANSFORMATION_1_STEPS)
        test_steps["Text file input"]["format"] = "Unix"
        trans.get_step_attribute("Text file input", "format")
        self.assertDictEqual(trans.steps, test_steps, "Error parsing steps")

        # Hops
        self.assertListEqual(trans.hops, constants.TRANSFORMATION_1_HOPS, "Error parsing hops")

        # Graph
        self.assertDictEqual(trans.graph, constants.TRANSFORMATION_1_GRAPH, "Error parsing graph")

        # Paths
        paths = [path for path in trans.find_all_paths("Text file input", "Text file output")]
        self.assertListEqual(paths, constants.TRANSFORMATION_1_PATHS)


if __name__ == "__main__":
    unittest.main()
