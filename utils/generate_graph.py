from typing import List
import networkx as nx
# import matplotlib.pyplot as plt


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
        excluded_nodes = []
        self.new_starting_points = []

        for component in self.parsed_netlist:
            if component.typeof == "top_instance":
                for sub_component in self.parsed_netlist:
                    if sub_component.name == component.parent:
                        for instance in sub_component.instances:
                            self.edges.append([sub_component, instance.name])
                        excluded_nodes = sub_component.name
                for each_tuple in starting_points:
                    temp_list = list(each_tuple)
                    if temp_list[0] == component.name:  # Handling weird top sub-circuit instantiation names
                        self.edges.append([component.name, component.parent])  # TODO: Better algo for top modules
                        if len(each_tuple) >= 3:
                            temp_list[0] = component.parent
                        self.new_starting_points.append(temp_list)
        if not self.new_starting_points:
            self.new_starting_points = starting_points
            for each_tuple in self.new_starting_points:
                for i in range(0, len(each_tuple) - 1):
                    self.edges.append([each_tuple[i], each_tuple[i + 1]])
            for component in self.parsed_netlist:
                if component.typeof == "SubCircuit":
                    if component.name not in excluded_nodes:
                        for each_instance in component.instances:
                            self.edges.append([component.name, each_instance.parent])
        else:
            for each_tuple in self.new_starting_points:
                for i in range(0, len(each_tuple) - 1):
                    self.edges.append([each_tuple[i], each_tuple[i + 1]])
                    excluded_nodes.append(each_tuple[i])
            for component in self.parsed_netlist:
                if component.typeof == "SubCircuit":
                    if component.name not in excluded_nodes:
                        for each_instance in component.instances:
                            self.edges.append([component.name, each_instance.parent])
        self.graph = nx.DiGraph(self.edges)

    # @property
    # def edge_coloring(self):
    #     return self.edge_colors
    #
    # def edge_weights(self):
    #     return self.weights

    # def plot_graph(self):
    #     plt.figure(1, figsize=(20, 20))
    #     pos = nx.shell_layout(self.graph)
    #     nx.draw(self.graph, pos,
    #             edge_color=self.edge_coloring,
    #             node_size=1000,
    #             width=self.edge_weights(),
    #             with_labels=True,
    #             node_color='lightgreen')
    #     plt.savefig("graph.pdf")
    #     plt.show()

    def generate_graph(self):
        return self.graph

    def find_path(self, starting_node):
        return list(nx.edge_bfs(self.graph, starting_node))

    def depth_dict(self, source):
        return nx.shortest_path_length(self.graph, source=source)
