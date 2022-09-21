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
        self.parsed_netlist = parsed_netlist
        self.edge_colors = []
        self.weights = []
        excluded_nodes = []
        starting_edges_color = "r"
        normal_edges_color = "b"
        starting_edges_weight = 1
        normal_edges_weight = 0.5
        self.new_starting_points = []
        for component in self.parsed_netlist:
            if component.typeof == "top_instance":
                for each_tuple in starting_points:
                    temp_list = list(each_tuple)
                    if temp_list[0] == component.name:  # Handling weird top sub-circuit instantiation names
                        self.edges.append([component.name, component.parent])  # TODO: Better algo for top modules
                        self.edge_colors.append(starting_edges_color)
                        self.weights.append(starting_edges_weight)
                        if len(each_tuple) >= 3:
                            temp_list[0] = component.parent
                        self.new_starting_points.append(temp_list)
        for each_tuple in self.new_starting_points:
            for i in range(0, len(each_tuple) - 1):
                self.edges.append([each_tuple[i], each_tuple[i + 1]])
                excluded_nodes.append(each_tuple[i])
                self.edge_colors.append(starting_edges_color)
                self.weights.append(starting_edges_weight)
        for component in self.parsed_netlist:
            if component.typeof == "SubCircuit":
                if component.name not in excluded_nodes:
                    for each_instance in component.instances:
                        self.edges.append([component.name, each_instance.parent])
                        self.edge_colors.append(normal_edges_color)
                        self.weights.append(normal_edges_weight)
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
        return list(nx.edge_bfs(self.graph, starting_node))

    def depth_dict(self, source):
        return nx.shortest_path_length(self.graph, source=source)

