from parsers.netlist_parser import *
from utils.propagate_param import PropagateParam as pp
from utils.generate_graph import GenerateGraph as gg
from parsers.def_parser import DefParser

file = open('netlist/netlist', 'r')
sample = file.read()
parsed_netlist = parse_netlist(sample)

obj = DefParser("netlist/sboxTOP.def", (150, 50), (200, 60))
fetched_instances = obj.region_fetch()


pp_obj = pp(parsed_netlist, fetched_instances, "vthadd", 1.0)
pp_obj.generate_netlist("generated_netlist")
