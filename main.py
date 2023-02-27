from parsers.netlist_parser import *
from utils.propagate_param import PropagateParam as pp
from parsers.def_parser import DefParser
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

file = open('netlist/single_sbox/netlist', 'r')
sample = file.read()
parsed_netlist = parse_netlist(sample)


# def_obj = DefParser("netlist/single_sbox/sbox.def", (0, 0), (200, 200))
# fetched_instances = def_obj.region_fetch()
# #print(fetched_instances)
# netlist_obj = pp(parsed_netlist, fetched_instances, "vthadd", 0.8)
# netlist_obj.generate_netlist("single_sbox/generated_netlist")


region_increment = 66
horizontal_segments = 6
vertical_segments = 6
rectangles = []
for i in range(horizontal_segments):
    for j in range(vertical_segments):
        rectangles.append(([j * 20, i * 20], [region_increment + j * 20, region_increment + i * 20]))

region_count = 0
number_of_inst = []
for rectangle in rectangles:
    print("Region", region_count)
    def_obj = DefParser("netlist/single_sbox/sbox.def", rectangle[0], rectangle[1])
    fetched_instances = def_obj.region_fetch()
    print(fetched_instances)
    number_of_inst.append(len(fetched_instances))
    netlist_obj = pp(parsed_netlist, fetched_instances, "vthadd", 0.5)
    netlist_obj.generate_netlist("single_sbox/generated_regional/regional_netlist" + str(region_count))
    region_count += 1
    del def_obj
    del netlist_obj

file = open('netlist/single_sbox/netlist', 'r')
sample = file.read()
parsed_netlist = parse_netlist(sample)

to_be_modfied = {('sbox', 'g51018__2683', 'XNR21'), ('sbox', 'g51015__9906', 'XNR21'),
                 ('sbox', 'g51008__9682', 'XNR21'), ('sbox', 'g51017__4547', 'XNR21'),
                 ('sbox', 'g51009__1474', 'XNR21'), ('sbox', 'g51010__3772', 'XNR21'),
                 ('sbox', 'g51007__4296', 'XNR21'), ('sbox', 'g51016__8780', 'XNR21'),
                 ('sbox', 'g50992__5019', 'NAND22'), ('sbox', 'g50991__7344', 'NOR21'), ('sbox', 'g51011', 'INV2'),
                 ('sbox', 'g51012', 'INV2'),
                 ('sbox', 'g50989__1840', 'NOR21'), ('sbox', 'g50990__2703', 'NAND22'), ('sbox', 'g51013', 'INV2'),
                 ('sbox', 'g50790__8780', 'NOR21'), ('sbox', 'g50994__1857', 'NAND22'),
                 ('sbox', 'g50993__5795', 'NOR22'),
                 ('sbox', 'g51002__5266', 'NAND22'), ('sbox', 'g51005__6083', 'NOR22'),
                 ('sbox', 'g50991__7344', 'NOR21'), ('sbox', 'g51004__2250', 'NOR21'),
                 ('sbox', 'g50992__5019', 'NAND22'),
                 ('sbox', 'g51003__7114', 'NAND22'), ('sbox', 'g51000__5953', 'NOR21'),
                 ('sbox', 'g51001__5703', 'NAND22'), ('sbox', 'g51006', 'INV2'), ('sbox', 'g50979__7344', 'NOR21'),
                 ('sbox', 'g50968__8757', 'NOR21'),
                 ('sbox', 'g50980__2683', 'NOR21'), ('sbox', 'g50978__7118', 'NAND22'),
                 ('sbox', 'g50967__7118', 'NAND22'), ('sbox', 'g50977__9682', 'NAND22')}

netlist_obj = pp(parsed_netlist, to_be_modfied, "vthadd", 0.5)
netlist_obj.generate_netlist("single_sbox/generated_precise")
del netlist_obj

number_of_inst = np.array(number_of_inst)
data = number_of_inst.reshape((6, 6))
# Create the heatmap
ax = sns.heatmap(data[::-1], cmap='Blues', annot=True, cbar=False, square=True)

# Customize the plot
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.title('number of fetched instance in each of the 36 regions')
plt.savefig('number_of_fetched_instances.pdf', dpi=300, bbox_inches='tight')
