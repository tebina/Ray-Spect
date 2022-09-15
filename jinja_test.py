import jinja2
from parsers.netlist_parser import *
import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()


file = open('netlist/netlist', 'r')
sample = file.read()

parsed_netlist = parse_netlist(sample)
# for i in range(len(parsed_netlist)):

for component in parsed_netlist:
    if component.typeof == "SubCircuit":
        for eachinstance in component.instances:
            G.add_edge(component.name, eachinstance.name)
            G.add_edge(eachinstance.name, eachinstance.parent)

H = nx.DiGraph(G)
subax1 = plt.figure(1)
nx.draw(H)
plt.show()




# templateLoader = jinja2.FileSystemLoader(searchpath="./")
# templateEnv = jinja2.Environment(loader=templateLoader)
# TEMPLATE_FILE = "templates/subcircuit_template.txt"
# template = templateEnv.get_template(TEMPLATE_FILE)
#
# output = template.render(parsed_netlist=parsed_netlist)
# print(output)