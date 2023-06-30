from utils.utility import find_path
import utils.netlist_handler as rh
import jinja2

"""
subckt modp ( d g s b )
"""


class ModelXray:
    def __init__(self, graph_object, n_shift, p_shift, static_leakage=0):
        self.graph_instance = graph_object.get_graph()
        self.netlist_buffer = graph_object.get_netlist_buffer()
        print(type(self.netlist_buffer))
        self.starting_points = [tuple(lst) for lst in graph_object.get_starting_points()]
        self.n_shift = n_shift
        self.p_shift = p_shift
        self.static_leakage = static_leakage
        self.propagation_paths = []
        for starting_point in self.starting_points:
            path = find_path(starting_point, self.graph_instance)
            self.propagation_paths.append(path)
        print(self.propagation_paths[0])

    def append_top_instance(self, name, pins_list, parent, parameters):
        self.netlist_buffer[name] = rh.TopInstance(name, parent, pins_list, parameters)

    def append_sub_circuit(self, name, nets, instances, parameters_line):
        self.netlist_buffer[name] = rh.SubCircuit(name, nets, instances, parameters_line)

    def append_instance(self, name, pins_list, parent, parameters):
        list_of_lists = [[key, value] for key, value in parameters.items()]
        return rh.Instance(name, pins_list, parent, list_of_lists)

    def propagate_model(self):
        for edge in self.propagation_paths[0]:
            if edge[0].typeof == "top_instance" and edge[1].typeof == "sub_circuit":
                continue
            elif edge[0].typeof == "sub_circuit" and edge[1].typeof == "instance":
                for instance in self.netlist_buffer["sub_circuit_" + edge[0].name].instances:
                    if instance.name == edge[1].name:
                        instance.name = "faulted_" + instance.name
                        instance.parent = "faulted_" + instance.parent
                        instance.nets.append(rh.Pin("v_fault", ""))
            elif edge[0].typeof == "sub_circuit" and edge[1].typeof == "sub_circuit":
                if not self.netlist_buffer["sub_circuit_" + edge[0].name].visited:
                    for instance in self.netlist_buffer["sub_circuit_" + edge[0].name].instances:
                        if instance.isNmos or instance.isPmos:
                            break
                        instance.name = "faulted_" + instance.name
                        instance.parent = "faulted_" + instance.parent

                    original_subcircuit_string = self.netlist_buffer["sub_circuit_" + edge[0].name].name
                    subcircuit_string = "faulted_" + self.netlist_buffer["sub_circuit_" + edge[0].name].name
                    self.netlist_buffer["sub_circuit_" + subcircuit_string] = self.netlist_buffer[
                        "sub_circuit_" + original_subcircuit_string]
                    self.netlist_buffer["sub_circuit_" + subcircuit_string].name = subcircuit_string
                    for index in range(len(self.netlist_buffer["sub_circuit_" + subcircuit_string].instances)):
                        instance = self.netlist_buffer["sub_circuit_" + subcircuit_string].instances[index]
                        instance = self.append_instance("faulted_" + instance.name, instance.nets.name,
                                                        "faulted_" + instance.parent, instance.parameters)

                if not self.netlist_buffer["sub_circuit_" + edge[0].name].visited:
                    instances = self.netlist_buffer["sub_circuit_faulted_" + edge[0].name].instances
                    vsource_increment = 0
                    for instance in self.netlist_buffer["sub_circuit_faulted_" + edge[0].name].instances:
                        if instance.isNmos or instance.isPmos:
                            vsource_increment += 1
                            grid_input = instance.nets[1].name
                            vsource_plus = "added_net_" + str(vsource_increment)
                            vsource_minus = grid_input
                            instance.nets[1].name = "added_net_" + str(vsource_increment)
                            instances.append(self.append_instance("added_vsource_" + str(vsource_increment),
                                                                  [vsource_plus, vsource_minus], "vsource",
                                                                  {"dc": str(self.n_shift), "type": "dc"}))
                    self.netlist_buffer["sub_circuit_faulted_" + edge[0].name].instances = instances
                    self.netlist_buffer["sub_circuit_" + edge[0].name].visited = True

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
