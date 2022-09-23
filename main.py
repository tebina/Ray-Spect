from parsers.netlist_parser import *
from utils.propagate_param import PropagateParam as pp

file = open('netlist/other_new_netlist', 'r')
sample = file.read()
parsed_netlist = parse_netlist(sample)

target_instances = [("sbox2","g50639__1857","OAI222") , ("sbox2","g50639__1857","OAI222") , ("sbox2","g50648__1309","AOI221") , ("sbox3","g50526","NAND31"),("sbox2", "g50660", "INV2"),("g48", "NAND31")]


pp_obj = pp(parsed_netlist, target_instances, "vthadd", 20)
pp_obj.generate_netlist()
