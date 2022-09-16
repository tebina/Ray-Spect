import jinja2
from parsers.netlist_parser import *
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

file = open('netlist/netlist', 'r')
sample = file.read()

parsed_netlist = parse_netlist(sample)
# for i in range(len(parsed_netlist)):


insts = ["g50488__4296", "g50534__1786", "g50439__1786", "g50930", "g51020__6877", "g50475__2250", "g50946__7118" , "g50990__5703" , "g50801__1857"]
for component in parsed_netlist:
    if component.typeof == "SubCircuit":

        if component.name == "sbox":
            for eachinstance in component.instances:
                for myinsts in insts:
                    if myinsts == eachinstance.name:
                        G.add_edge(myinsts, eachinstance.parent, color='r', weight=1)
        elif component.name != "sbox_1" and component.name != "sbox_2":
            for eachinstance in component.instances:
                #print (component.name, "=====>", eachinstance.parent)
                G.add_edge(component.name, eachinstance.parent, color='b', weight=0.5)



# print(list(G.successors("NAND22")))



print (list(nx.dfs_tree(G,"g50534__1786").edges()))

print (list(G.nodes))

colors = nx.get_edge_attributes(G,'color').values()
weights = nx.get_edge_attributes(G,'weight').values()
plt.figure(1,figsize=(20,20))
pos = nx.circular_layout(G)
nx.draw(G, pos,
        edge_color=colors,
        node_size=1000,
        width=list(weights),
        with_labels=True,
        node_color='lightgreen')
plt.savefig("graph.pdf")
plt.show()

# plt.figure(figsize=(9, 9))
# nx.draw_spring(G, with_labels=True)
# plt.savefig("graph.pdf")
# plt.axis("equal")
# plt.show()
# #


# templateLoader = jinja2.FileSystemLoader(searchpath="./")
# templateEnv = jinja2.Environment(loader=templateLoader)
# TEMPLATE_FILE = "templates/subcircuit_template.txt"
# template = templateEnv.get_template(TEMPLATE_FILE)
#
# output = template.render(parsed_netlist=parsed_netlist)
# print(output)
