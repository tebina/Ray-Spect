from typing import List

from parsers.netlist_parser import parse_netlist
import networkx as nx
import matplotlib.pyplot as plt


class GenerateGraph:

    edge_colors: List[str]

    def __init__(self, parsed_netlist, starting_points):
        """
        -staring tuples (A,B,C) are converted into edges (A,B) (B,C) (C,D)
        -Adding all nodes from starting tuple members to the excluded sub-circuits to parse
        into the netlist tree, except the last element (A, B, C) ==> (A, B) excluded / (C) kept
        :type parsed_netlist: object
        :param parsed_netlist:
        :param starting_points:
        """
        self.edges = []
        self.parsed_netlist = parse_netlist(parsed_netlist)
        self.starting_points = starting_points
        self.excluded_nodes = []
        self.edge_colors = []
        self.weights = []
        for each_tuple in self.starting_points:
            for i in range(0, len(each_tuple) - 1):
                self.edges.append([each_tuple[i], each_tuple[i + 1]])
                self.excluded_nodes.append(each_tuple[i])
                self.edge_colors.append("r")
                self.weights.append(1)
        for component in self.parsed_netlist:
            if component.typeof == "SubCircuit":
                if component.name not in self.excluded_nodes:
                    for each_instance in component.instances:
                        self.edges.append([component.name, each_instance.parent])
                        self.edge_colors.append("b")
                        self.weights.append(0.5)

        self.graph = nx.DiGraph(self.edges)

    @property
    def edge_coloring(self):
        return self.edge_colors

    def edge_weights(self):
        return self.weights

    def plot_graph(self):
        plt.figure(1, figsize=(20, 20))
        pos = nx.shell_layout(self.graph)
        nx.draw(self.graph, pos,
                edge_color=self.edge_coloring,
                node_size=1000,
                width=self.edge_weights(),
                with_labels=True,
                node_color='lightgreen')
        plt.savefig("graph.pdf")
        plt.show()

    def generate_graph(self):
        return self.graph

    def find_path(self, starting_node):
        return list(nx.dfs_tree(self.graph, starting_node).edges())
