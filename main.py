from parsers.netlist_parser import *
from utils.propagate_param import PropagateParam as pp
from utils.generate_graph import GenerateGraph as gg
from parsers.def_parser import region_fetch

file = open('netlist/netlist', 'r')
sample = file.read()
parsed_netlist = parse_netlist(sample)

fetched_instances = region_fetch("netlist/sboxTOP.def", (150, 50), (250, 200))


# pp_obj = pp(parsed_netlist, fetched_instances, "vthadd", 1.0)
# pp_obj.generate_netlist("netlist1")
