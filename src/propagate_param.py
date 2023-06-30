import jinja2
import networkx as nx

from utils.utility import netlist_to_dict


class PropagateParam:

    def __init__(self, graph_object, parameter, value):
        self.parameter = parameter
        self.value = value
        self.graph_instance = graph_object.get_graph()
        self.netlist_buffer = graph_object.get_netlist_buffer()
        self.starting_points = graph_object.get_starting_points()
        print(self.starting_points)
        self.propagate_param(self.starting_points[0])
        self.previous_fetch = self.netlist_buffer

    def propagate_param(self, starting_point):
        components = self.netlist_buffer
        for node in starting_point:
            match node.typeof:
                case "top_instance":
                    if components["top_instance_" + node.name].visited is False:
                        components["top_instance_" + node.name].parameters[self.parameter] = self.value
                        components["top_instance_" + node.name].visited = True
                        self.previous_fetch = components["top_instance_" + node.name]
                case "instance":
                    if components["sub_circuit_" + self.previous_fetch.parent].isParameterEmpty is False:
                        components["sub_circuit_" + self.previous_fetch.parent].parameters[self.parameter] = 0
                        components["sub_circuit_" + self.previous_fetch.parent].visited = True
                    for instance in components["sub_circuit_" + self.previous_fetch.parent].instances:
                        if node.name == instance.name:
                            instance.parameters[self.parameter] = self.parameter
                case "sub_circuit":
                    while
                    if components["sub_circuit_" + node.name].isParameterEmpty is False:
                        components["sub_circuit_" + node.name].parameters[self.parameter] = 0
                        components["sub_circuit_" + node.name].visited = True

            # path_tuples = list(nx.edge_bfs(self.graph_instance, node[0].name))
            # print(path_tuples)

            return self.netlist_buffer

            # for edge in path_tuples:
            #     for component in self.netlist_buffer:
            #         if component.typeof == "SubCircuit":
            #             if component.visited is False and component.name == edge[0]:
            #                 component.parameters += f" {self.parameter}=0"
            #                 component.visited = True
            #             if component.name == edge[0]:
            #                 for instance in component.instances:
            #                     if instance.name == edge[1]:
            #                         instance.parameters[
            #                             self.parameter] = self.value
            #                     elif instance.parent == edge[1]:
            #                         instance.parameters[
            #                             self.parameter] = self.parameter
            #         if component.typeof == "top_instance":
            #             if component.visited is False:
            #                 if component.name == edge[0]:
            #                     component.parameters[self.parameter] = self.value
            #                     component.visited = True

    def generate_netlist(self, generated_netlist_name):
        """
        Generate a aes_sbox_netlist from the aes_sbox_netlist buffer.

        This function takes a aes_sbox_netlist buffer input and produces a aes_sbox_netlist file. The aes_sbox_netlist file can be used for
        further circuit simulation or design.
        """
        template_loader = jinja2.FileSystemLoader(searchpath="./")
        template_env = jinja2.Environment(loader=template_loader)
        template_file = "./templates/subcircuit_template"
        template = template_env.get_template(template_file)
        output = template.render(parsed_netlist=self.propagate_param())
        f = open(generated_netlist_name, "w")
        f.write(output)
        f.close()
