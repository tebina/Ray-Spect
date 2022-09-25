from parsers.netlist_parser import *
from utils.propagate_param import PropagateParam as pp
from parsers.def_parser import def_parser
file = open('netlist/netlist', 'r')
sample = file.read()
parsed_netlist = parse_netlist(sample)

target_instances = [("sbox2","g50639__1857","OAI222") , ("sbox2","g50639__1857","OAI222") , ("sbox2","g50648__1309","AOI221") , ("sbox3","g50526","NAND31"),("sbox2", "g50660", "INV2"),("g48", "NAND31")]
new_target_instances = []
mytuples = def_parser("netlist/sboxTOP.def")
for tuples in mytuples:
    if "FILLER" in tuples[0][0]:
        continue
    new_target_instances.append(tuples[0])


print (len(new_target_instances))
pp_obj = pp(parsed_netlist, new_target_instances[0:100], "vthadd", 90)
pp_obj.generate_netlist()
