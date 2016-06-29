import copy
import unittest
import KettleParser
import constants

__author__ = 'jeffportwood'

class KettleParserTests(unittest.TestCase):

    def test_parse_xml_file(self):
        trans = KettleParser.ParseKettleXml(constants.TRANSFORMATION_1_FILE)

        # Steps
        test_steps = copy.deepcopy(constants.TRANSFORMATION_1_STEPS)
        self.assertDictEqual(trans.steps, test_steps, "Error parsing steps")

        # Hops
        self.assertListEqual(trans.hops, constants.TRANSFORMATION_1_HOPS, "Error parsing hops")

        # Graph
        self.assertDictEqual(trans.graph, constants.TRANSFORMATION_1_GRAPH, "Error parsing graph")

    def test_parse_xml_raw(self):
        trans = KettleParser.ParseKettleXml(constants.TRANSFORMATION_1_XML.strip(), is_file=False)

        # Steps
        test_steps = copy.deepcopy(constants.TRANSFORMATION_1_STEPS)
        self.assertDictEqual(trans.steps, test_steps, "Error parsing steps")

        # Hops
        self.assertListEqual(trans.hops, constants.TRANSFORMATION_1_HOPS, "Error parsing hops")

        # Graph
        self.assertDictEqual(trans.graph, constants.TRANSFORMATION_1_GRAPH, "Error parsing graph")


    def test_valid_file_type(self):
        self.assertEquals(KettleParser.ParseKettleXml(constants.TRANSFORMATION_1_FILE).file_type, "transformation")


    def test_get_step_attribute(self):
        test_steps = copy.deepcopy(constants.TRANSFORMATION_1_STEPS)
        test_steps["Text file input"]["format"] = "Unix"

        trans = KettleParser.ParseKettleXml(constants.TRANSFORMATION_1_FILE)
        trans.get_step_attribute("Text file input", "format")

        self.assertDictEqual(trans.steps, test_steps, "Error parsing steps")


if __name__ == "__main__":
    unittest.main()
