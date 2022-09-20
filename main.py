from parsers.netlist_parser import *
from utils.generate_graph import GenerateGraph

file = open('netlist/netlist', 'r')
sample = file.read()
parsed_netlist = parse_netlist(sample)

target_instances = [("sbox2", "g50835", "INV2"), ("sbox1", "g50868__1474", "NAND22"),
                    ("sbox1", "g50982__7118", "NAND23"), ("sbox1", "g50437__1840", "NAND31") , ("g44", "NAND31"), ("sbox3","g51021","NOR31")]

graph_instance = GenerateGraph(sample, target_instances)
graph_instance.plot_graph()

# templateLoader = jinja2.FileSystemLoader(searchpath="./")
# templateEnv = jinja2.Environment(loader=templateLoader)
# TEMPLATE_FILE = "templates/subcircuit_template.txt"
# template = templateEnv.get_template(TEMPLATE_FILE)
#
# output = template.render(parsed_netlist=parsed_netlist)
# print(output)
