import jinja2
from parsers.netlist_parser import *
import networkx as nx
from generate_graph import GenerateGraph

file = open('netlist/netlist', 'r')
sample = file.read()
parsed_netlist = parse_netlist(sample)

target_instances = [("sbox_2", "g50835", "INV2"), ("sbox_1", "g50868__1474", "NAND22"),
                    ("sbox", "g50982__7118", "NAND23"), ("sbox_1", "g50437__1840", "NAND31")]

object = GenerateGraph(sample, target_instances)
object.plot_graph()

print (object.find_path("sbox_1"))

# templateLoader = jinja2.FileSystemLoader(searchpath="./")
# templateEnv = jinja2.Environment(loader=templateLoader)
# TEMPLATE_FILE = "templates/subcircuit_template.txt"
# template = templateEnv.get_template(TEMPLATE_FILE)
#
# output = template.render(parsed_netlist=parsed_netlist)
# print(output)
