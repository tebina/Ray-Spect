from utils.utility import find_path
import utils.netlist_handler as rh
import jinja2
import copy

"""
subckt modp ( d g s b )
"""


class ModelXray:
    def __init__(self, graph_object, n_shift, p_shift, static_leakage=0):
        self.graph_instance = graph_object.get_graph()
        print(self.graph_instance.edges)
        self.netlist_buffer = graph_object.get_netlist_buffer()
        self.starting_points = [tuple(lst) for lst in graph_object.get_starting_points()]
        print(self.starting_points)
        self.unique_instances = []
        for starting_tuple in self.starting_points:
            if len(starting_tuple) == 2 and starting_tuple[0].typeof == "top_instance":
                self.unique_instances.append(starting_tuple[0].name)
        self.n_shift = n_shift
        self.p_shift = p_shift
        self.static_leakage = static_leakage
        self.propagation_paths = []
        for starting_point in self.starting_points:
            path = find_path(starting_point, self.graph_instance)
            if path not in self.propagation_paths:
                self.propagation_paths.append(path)
        self.propagation_paths_tuples = [item for sublist in self.propagation_paths for item in sublist]

    def append_top_instance(self, name, pins_list, parent, parameters):
        self.netlist_buffer[name] = rh.TopInstance(name, parent, pins_list, parameters)

    def append_sub_circuit(self, name, nets, instances, parameters_line):
        self.netlist_buffer[name] = rh.SubCircuit(name, nets, instances, parameters_line)

    def append_instance(self, name, pins_list, parent, parameters):
        list_of_lists = [[key, value] for key, value in parameters.items()]
        return rh.Instance(name, pins_list, parent, list_of_lists)

    def handle_subcircuit_instance(self, edge):
        for instance in self.netlist_buffer["sub_circuit_" + edge[0].name].instances:
            if instance.name == edge[1].name:
                instance.name = "faulted_" + instance.name
                instance.parent = "faulted_" + instance.parent

    def copy_subcircuit(self, new_component, reference_component):
        self.netlist_buffer["sub_circuit_" + new_component] = copy.deepcopy(
            self.netlist_buffer["sub_circuit_" + reference_component])

    def fix_component_buffer_name(self, name):
        self.netlist_buffer["sub_circuit_" + name].name = name

    def fault_instances(self, instances_list):
        for instance in instances_list:
            if instance.isNmos or instance.isPmos:
                break
            instance.name = "faulted_" + instance.name
            instance.parent = "faulted_" + instance.parent

    def handle_voltage_sources(self, instances_list, edge):
        vsource_increment = 0
        instances = instances_list
        for instance in instances_list:
            if instance.isNmos or instance.isPmos:
                vsource_increment += 1
                grid_input = instance.nets[1].name
                vsource_plus = "added_net_" + str(vsource_increment)
                vsource_minus = grid_input
                instance.nets[1].name = "added_net_" + str(vsource_increment)
                instances.append(
                    self.append_instance("added_vsource_" + str(vsource_increment),
                                         [vsource_plus, vsource_minus],
                                         "vsource",
                                         {"dc": str(self.n_shift), "type": "dc"}))
        self.netlist_buffer["sub_circuit_faulted_" + edge[0].name].instances = instances

    def handle_subcircuit_subcircuit(self, edge):
        original_subcircuit_string = self.netlist_buffer["sub_circuit_" + edge[0].name].name
        faulted_subcircuit_string = "faulted_" + original_subcircuit_string
        self.copy_subcircuit(faulted_subcircuit_string, original_subcircuit_string)
        self.fix_component_buffer_name(faulted_subcircuit_string)

        faulted_instances = self.netlist_buffer["sub_circuit_" + faulted_subcircuit_string].instances
        self.fault_instances(faulted_instances)
        self.handle_voltage_sources(faulted_instances, edge)
        self.netlist_buffer["sub_circuit_" + edge[0].name].visited = True

    def handle_topinstance_subcircuit(self, edge):
        top_instance_name = self.netlist_buffer["top_instance_" + edge.name].name
        top_instance_parent = self.netlist_buffer["top_instance_" + edge.name].parent
        self.netlist_buffer["top_instance_" + edge.name].name = "faulted_" + top_instance_name
        self.netlist_buffer["top_instance_" + edge.name].parent = "faulted_" + top_instance_parent
        self.netlist_buffer["top_instance_" + edge.name].visited = True

    def propagate_model(self):
        for edge in self.propagation_paths_tuples:
            if edge[0].typeof == "top_instance" and edge[1].typeof == "sub_circuit":
                if edge[0].name in self.unique_instances and not self.netlist_buffer["top_instance_" + edge[0].name].visited:
                    print("is")
                    self.handle_topinstance_subcircuit(edge[0])
                else:
                    continue

            elif edge[0].typeof == "sub_circuit" and edge[1].typeof == "instance":
                self.handle_subcircuit_instance(edge)

            elif edge[0].typeof == "sub_circuit" and edge[1].typeof == "sub_circuit":
                if not self.netlist_buffer["sub_circuit_" + edge[0].name].visited:
                    self.handle_subcircuit_subcircuit(edge)
        return self.netlist_buffer.values()

    def generate_netlist(self, generated_netlist_name):
        """
        Generate a aes_sbox_netlist from the aes_sbox_netlist buffer.

        This function takes a aes_sbox_netlist buffer input and produces a aes_sbox_netlist file. The aes_sbox_netlist file can be used for
        further circuit simulation or design.
        """
        template_loader = jinja2.FileSystemLoader(searchpath="./")
        template_env = jinja2.Environment(loader=template_loader)
        template_file = "templates/subcircuit_template"
        template = template_env.get_template(template_file)
        output = template.render(parsed_netlist=self.propagate_model())
        f = open(generated_netlist_name, "w")
        f.write(output)
        f.close()
