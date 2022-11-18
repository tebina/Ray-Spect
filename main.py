from parsers.netlist_parser import *
from utils.propagate_param import PropagateParam as pp
from parsers.def_parser import DefParser


file = open('netlist/triple_sbox/netlist', 'r')
sample = file.read()
parsed_netlist = parse_netlist(sample)


region_increment = 20
horizontal_segments = 10
vertical_segments = 10
rectangles = []
for i in range(horizontal_segments):
    for j in range(vertical_segments):
        rectangles.append(([j * 20, i * 20], [region_increment + j * 20, region_increment + i * 20]))

region_count = 0
for rectangle in rectangles:
    region_count += 1
    def_obj = DefParser("netlist/triple_sbox/sboxTOP.def", rectangle[0], rectangle[1])
    fetched_instances = def_obj.region_fetch()
    netlist_obj = pp(parsed_netlist, fetched_instances, "vthadd", 0.8)
    netlist_obj.generate_netlist("generated_regional_netlists/regional_netlist" + str(region_count))

    del def_obj
    del netlist_obj

# def_obj = DefParser("netlist/sbox.def", (0, 0), (400, 400))
# fetched_instances = def_obj.region_fetch()
# netlist_obj = pp(parsed_netlist, fetched_instances, "vthadd", 0.8)
# netlist_obj.generate_netlist("generated_netlist0")

