from parsers.netlist_parser import *
from utils.propagate_param import PropagateParam as pp

file = open('netlist/other_new_netlist', 'r')
sample = file.read()
parsed_netlist = parse_netlist(sample)

target_instances = [("sbox3", "g50992", "NAND22"), ("sbox2", "g50717", "INV2"),
                    ("sbox2", "g50675__1840", "NOR21"), ("sbox2", "g50664", "INV2"),
                    ("sbox3", "g51021", "NOR31"), ("sbox2","g50639__1857","OAI222") , ("sbox2","g50639__1857","OAI222") , ("sbox2","g50648__1309","AOI221") , ("sbox2", "g50660", "INV2")]


pp_obj = pp(parsed_netlist, target_instances, "vthadd", 20)
pp_obj.generate_netlist()
