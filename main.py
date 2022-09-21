from parsers.netlist_parser import *
from utils.generate_graph import GenerateGraph

from utils.propagate_param import PropagateParam as pp

import jinja2

file = open('netlist/netlist', 'r')
sample = file.read()
parsed_netlist = parse_netlist(sample)

target_instances = [("sbox3", "g50992", "NAND22"), ("sbox2", "g50717", "INV2"),
                    ("sbox2", "g50675__1840", "NOR21"), ("sbox2", "g50664", "INV2"), ("g44", "NAND31"),
                    ("sbox3", "g51021", "NOR31")]


pp_obj = pp(parsed_netlist, target_instances, 0, 0)
pp_obj.depth_check()
pp_obj.generate_netlist()



#
# for edge in path:
#     for component in parsed_netlist:
#         if component.typeof == "SubCircuit":
#             if component.name == edge[0]:
#                 component.parameters += " pipi=kaki"
#                 for instance in component.instances:
#                     if instance.name == edge[1] or instance.parent == edge[1]:
#                         instance.many_parameters["pipi"] = "kaki"
#
#
#
#
#

#
# templateLoader = jinja2.FileSystemLoader(searchpath="./")
# templateEnv = jinja2.Environment(loader=templateLoader)
# TEMPLATE_FILE = "templates/subcircuit_template.txt"
# template = templateEnv.get_template(TEMPLATE_FILE)
# #
# output = template.render(parsed_netlist=parsed_netlist)
# # print(output)
# f = open("generated_netlist", "w")
# f.write(output)
# f.close()
