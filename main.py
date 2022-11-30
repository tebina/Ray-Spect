from parsers.netlist_parser import *
from utils.propagate_param import PropagateParam as pp
from parsers.def_parser import DefParser


file = open('netlist/single_sbox/netlist', 'r')
sample = file.read()
parsed_netlist = parse_netlist(sample)


def_obj = DefParser("netlist/single_sbox/sbox.def", (0, 0), (200, 200))
fetched_instances = def_obj.region_fetch()
#print(fetched_instances)
netlist_obj = pp(parsed_netlist, fetched_instances, "vthadd", 0.8)
netlist_obj.generate_netlist("single_sbox/generated_netlist")



region_increment = 80
horizontal_segments = 5
vertical_segments = 5
rectangles = []
for i in range(horizontal_segments):
    for j in range(vertical_segments):
        rectangles.append(([j * 20, i * 20], [region_increment + j * 20, region_increment + i * 20]))

# region_count = 0
# for rectangle in rectangles:
#     region_count += 1
#     print("Region", region_count)
#     def_obj = DefParser("netlist/single_sbox/sbox.def", rectangle[0], rectangle[1])
#     fetched_instances = def_obj.region_fetch()
#     netlist_obj = pp(parsed_netlist, fetched_instances, "vthadd", 0.8)
#     netlist_obj.generate_netlist("single_sbox/generated_regional/regional_netlist" + str(region_count))
#
#     del def_obj
#     del netlist_obj


