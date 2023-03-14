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

def count_occurrences(lst, element):
    count = 0
    for item in lst:
        if isinstance(item, list):
            count += count_occurrences(item, element)
        else:
            if item == element:
                count += 1
    return count


region_increment = 50
horizontal_segments = 8
vertical_segments = 8
rectangles = []
for i in range(horizontal_segments):
    for j in range(vertical_segments):
        rectangles.append(([j * region_increment, i * region_increment],
                           [region_increment + j * region_increment, region_increment + i * region_increment]))

region_count = 0
number_of_inst = []
number_of_xnor = []
number_of_inv = []

number_of_nand22 = []
number_of_nand41 = []
number_of_nand31 = []

number_of_nor21 = []
number_of_nor40 = []

number_of_dfc3 = []
number_of_clkbuf = []

for rectangle in rectangles:
    parsed_netlist = parse_netlist(sample)
    print("Region", region_count)
    def_obj = DefParser("netlist/single_sbox/sbox.def", rectangle[0], rectangle[1])
    fetched_instances = def_obj.region_fetch()
    print(fetched_instances)
    number_of_inst.append(len(fetched_instances))

    number_of_xnor.append(count_occurrences(fetched_instances, "XNR21"))
    number_of_inv.append(count_occurrences(fetched_instances, "INV2"))
    number_of_nand22.append(count_occurrences(fetched_instances, "NAND22"))
    number_of_nor21.append(count_occurrences(fetched_instances, "NOR21"))

    number_of_nand41.append(count_occurrences(fetched_instances, "NAND41"))
    number_of_nand31.append(count_occurrences(fetched_instances, "NAND31"))
    number_of_nor40.append(count_occurrences(fetched_instances, "NOR40"))
    number_of_dfc3.append(count_occurrences(fetched_instances, "DFC3"))
    number_of_clkbuf.append(count_occurrences(fetched_instances,"CLKBU2"))

    netlist_obj = pp(parsed_netlist, fetched_instances, "vthadd", 0.5)
    netlist_obj.generate_netlist("single_sbox/generated_regional/regional_netlist" + str(region_count))
    region_count += 1
    del def_obj
    del netlist_obj

# file = open('netlist/single_sbox/netlist', 'r')
# sample = file.read()
# parsed_netlist = parse_netlist(sample)
#
# to_be_modfied = {('sbox', 'reg_reg\[0\]', 'DFC3'), ('sbox', 'reg_reg\[1\]', 'DFC3'), ('sbox', 'reg_reg\[2\]', 'DFC3'),
#                  ('sbox', 'reg_reg\[3\]', 'DFC3'), ('sbox', 'reg_reg\[4\]', 'DFC3'), ('sbox', 'reg_reg\[5\]', 'DFC3'),
#                  ('sbox', 'reg_reg\[6\]', 'DFC3'), ('sbox', 'reg_reg\[7\]', 'DFC3') }
#
# netlist_obj = pp(parsed_netlist, to_be_modfied, "vthadd", 0.5)
# netlist_obj.generate_netlist("single_sbox/generated_precise")
# del netlist_obj

number_of_inst = np.array(number_of_inst)
data = number_of_inst.reshape((8, 8))
# # Create the heatmap
ax = sns.heatmap(data[::-1], cmap='Blues', annot=True, cbar=False, square=True)
#
# # Customize the plot
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.title('number of fetched instance in each of the 64 regions')
plt.savefig('pdf/number_of_fetched_instances.pdf', dpi=300, bbox_inches='tight')
plt.close()

number_of_xnor = np.array(number_of_xnor)
number_of_inv = np.array(number_of_inv)
number_of_nand22 = np.array(number_of_nand22)
number_of_nor21 = np.array(number_of_nor21)

number_of_nand41 = np.array(number_of_nand41)
number_of_nand31 = np.array(number_of_nand31)
number_of_nor40 = np.array(number_of_nor40)
number_of_dfc3 = np.array(number_of_dfc3)
number_of_clkbuf = np.array(number_of_clkbuf)

data2 = number_of_xnor.reshape((8, 8))
data3 = number_of_inv.reshape((8, 8))
data4 = number_of_nand22.reshape((8, 8))
data5 = number_of_nor21.reshape((8, 8))

data6 = number_of_nand41.reshape((8, 8))
data7 = number_of_nand31.reshape((8, 8))
data8 = number_of_nor40.reshape((8, 8))
data9 = number_of_dfc3.reshape((8, 8))
data10 = number_of_clkbuf.reshape((8, 8))

ax = sns.heatmap(data2[::-1], cmap='Blues', annot=True, cbar=False, square=True)
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.title('number of fetched XNOR in each of the 64 regions')
plt.savefig('pdf/number_of_fetched_XNOR_instances.pdf', dpi=300, bbox_inches='tight')
plt.close()

ax = sns.heatmap(data3[::-1], cmap='Blues', annot=True, cbar=False, square=True)
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.title('number of fetched INV in each of the 64 regions')
plt.savefig('pdf/number_of_fetched_INV_instances.pdf', dpi=300, bbox_inches='tight')
plt.close()

ax = sns.heatmap(data4[::-1], cmap='Blues', annot=True, cbar=False, square=True)
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.title('number of fetched NAND in each of the 64 regions')
plt.savefig('pdf/number_of_fetched_NAND_instances.pdf', dpi=300, bbox_inches='tight')
plt.close()

ax = sns.heatmap(data5[::-1], cmap='Blues', annot=True, cbar=False, square=True)
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.title('number of fetched NOR in each of the 64 regions')
plt.savefig('pdf/number_of_fetched_NOR_instances.pdf', dpi=300, bbox_inches='tight')
plt.close()

##################################
ax = sns.heatmap(data6[::-1], cmap='Blues', annot=True, cbar=False, square=True)
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.title('number of fetched NAND41 in each of the 64 regions')
plt.savefig('pdf/number_of_fetched_NAND41_instances.pdf', dpi=300, bbox_inches='tight')
plt.close()

ax = sns.heatmap(data7[::-1], cmap='Blues', annot=True, cbar=False, square=True)
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.title('number of fetched NAND31 in each of the 64 regions')
plt.savefig('pdf/number_of_fetched_NAND31_instances.pdf', dpi=300, bbox_inches='tight')
plt.close()

ax = sns.heatmap(data8[::-1], cmap='Blues', annot=True, cbar=False, square=True)
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.title('number of fetched NOR40 in each of the 64 regions')
plt.savefig('pdf/number_of_fetched_NOR40_instances.pdf', dpi=300, bbox_inches='tight')
plt.close()

ax = sns.heatmap(data9[::-1], cmap='Blues', annot=True, cbar=False, square=True)
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.title('number of fetched DFC3 in each of the 64 regions')
plt.savefig('pdf/number_of_fetched_DFC3_instances.pdf', dpi=300, bbox_inches='tight')
plt.close()

ax = sns.heatmap(data10[::-1], cmap='Blues', annot=True, cbar=False, square=True)
ax.set_xticklabels([])
ax.set_yticklabels([])
plt.title('number of fetched CLKBUF in each of the 64 regions')
plt.savefig('pdf/number_of_fetched_CLKBUF_instances.pdf', dpi=300, bbox_inches='tight')
plt.close()
