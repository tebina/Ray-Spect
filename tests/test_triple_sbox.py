from parsers.netlist_parser import *
from utils.propagate_param import PropagateParam as propagate_param
from parsers.def_parser import DefParser
import unittest


class TestString(unittest.TestCase):
    def test_is_file_empty(self):
        file = open('tests/input_files/triple_aes_sbox/aes_sbox_netlist', 'r')
        sample = file.read()
        self.assertNotEqual(len(sample), 0)

    def test_is_parsed_file_empty(self):
        file = open('tests/input_files/triple_aes_sbox/aes_sbox_netlist', 'r')
        sample = file.read()
        parsed_netlist = parse_netlist(sample)
        self.assertNotEqual(parsed_netlist, [])

    def test_is_parsed_def_empty(self):
        parsed_def = DefParser("tests/input_files/triple_aes_sbox/aes_sbox.def", (0, 0), (480, 480)).region_fetch()
        self.assertEqual(parsed_def[len(parsed_def) - 1], ['g48', 'NAND31'])

    def test_propagate_param(self):
        file = open('tests/input_files/triple_aes_sbox/aes_sbox_netlist', 'r')
        sample = file.read()
        parsed_netlist = parse_netlist(sample)
        parsed_def = DefParser("tests/input_files/triple_aes_sbox/aes_sbox.def", (50, 50), (55, 55)).region_fetch()
        netlist_obj = propagate_param(parsed_netlist, parsed_def, "vthadd", 0.8).propagate_param()
        for component in netlist_obj:
            if component.name == "inv_core":
                self.assertTrue("vthadd=0" in component.parameters)
                self.assertTrue(component.instances[0][3]['vthadd'] == 'vthadd')
                self.assertTrue(component.instances[1][3]['vthadd'] == 'vthadd')
            if component.name == "INV2":
                self.assertTrue("vthadd=0" in component.parameters)
                self.assertTrue(component.instances[0][3]['vthadd'] == 'vthadd')
            if component.name == "sbox2" and component.typeof == "SubCircuit":
                self.assertTrue("vthadd=0" in component.parameters)
                for instance in component.instances:
                    if instance[0] == "g50664":
                        self.assertEqual(0.8, instance[3]["vthadd"],
                                         msg="Propagate param error => didn't propagate parameters in sbox2")
                    break
            if component.name == "sbox2" and component.typeof == "top_instance":
                self.assertEqual(0.8, component.parameters["vthadd"])


if __name__ == "__main__":
    unittest.main()
