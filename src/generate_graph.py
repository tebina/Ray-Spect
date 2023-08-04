import matplotlib.pyplot as plt
import networkx as nx

from parsers.def_parser import DefParser
from parsers.netlist_parser import *
from utils.utility import netlist_to_dict
from utils.def_handler import *


class GenerateGraph:

    def __init__(self, netlist_file, def_file, region_point1, region_point2):
        file = open(netlist_file, 'r')
        self.parsed_netlist = netlist_to_dict(parse_netlist(file.read()))
        self.edge_colors = []
        self.weights = []
        self.starting_edges_color = "r"
        self.normal_edges_color = "b"
        self.starting_edges_weight = 2
        self.normal_edges_weight = 1
        self.edges = []
        self.def_instance = DefParser(def_file, region_point1, region_point2)
        self.starting_points = self.def_instance.region_fetch()
        filtered_starting_points = self.graph_preprocess()
        for starting_point in filtered_starting_points:
            self.traverse_netlist(starting_point.name)
        self.edges = list(set(tuple(sublist) for sublist in self.edges))
        self.graph = nx.DiGraph(self.edges)

    def get_graph(self):
        return self.graph

    def get_starting_points(self):
        return self.starting_points

    def get_netlist_buffer(self):
        return self.parsed_netlist

    def plot_graph(self):
        plt.figure(1, figsize=(20, 20))
        pos = nx.shell_layout(self.graph)
        nx.draw(self.graph, pos,
                edge_color=self.edge_colors,
                node_size=1000,
                width=self.weights,
                with_labels=True,
                node_color='lightgreen')
        plt.savefig("graph.pdf")
        plt.show()

    def plot_region(self):
        self.def_instance.plot_region()

    def graph_preprocess(self):
        new_starting_points = []
        for starting_point in self.starting_points:
            match len(starting_point):
                case 2:
                    component0 = TopInstance(self.parsed_netlist["top_instance_" + starting_point[0].name].name)
                    component1 = SubCircuit(self.parsed_netlist["top_instance_" + starting_point[0].name].parent)
                    self.edges.append((component0, component1))
                    self.edge_colors.append(self.starting_edges_color)
                    self.weights.append(self.starting_edges_weight)
                    new_starting_points.append(component1)
                case 3:
                    component1 = TopInstance(self.parsed_netlist["top_instance_" + starting_point[0].name].name)
                    component2 = SubCircuit(self.parsed_netlist["top_instance_" + starting_point[0].name].parent)
                    self.edges.append((component1, component2))
                    component3 = Instance(starting_point[1].name)
                    component4 = SubCircuit(starting_point[2].name)
                    self.edges.append((component2, component3))
                    self.edges.append((component3, component4))
                    new_starting_points.append(component4)
                    self.edge_colors.extend([self.starting_edges_color] * 3)
                    self.weights.extend([self.starting_edges_weight] * 3)
                case _:
                    assert "not implemented yet ! "
        return list(new_starting_points)

    def traverse_netlist(self, starting_point):
        for instance in self.parsed_netlist["sub_circuit_" + starting_point].instances:
            component1 = SubCircuit(starting_point)
            component2 = SubCircuit(instance.parent)
            self.edges.append((component1, component2))
            self.edge_colors.append(self.normal_edges_color)
            self.weights.append(self.normal_edges_weight)
            if instance.isPmos is False and instance.isNmos is False:
                self.traverse_netlist(instance.parent)
