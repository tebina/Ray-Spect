from utils.generate_graph import GenerateGraph
import jinja2


class PropagateParam:

    def __init__(self, parsed_netlist, starting_points, parameter, value):
        self.netlist_buffer = parsed_netlist
        self.starting_points = starting_points
        self.parameter = parameter
        self.value = value
        self.graph_instance = GenerateGraph(self.netlist_buffer, self.starting_points)

    def depth_check(self):
        depths = []
        for tuples in self.starting_points:
            depths.append(self.graph_instance.depth_dict(tuples[0]).values())
        print(depths)

    def propagate_param(self):
        """
        This function propagates parameters from one circuit in a netlist to another circuit. The first circuit in
        the netlist is the source circuit, and the second circuit is the target circuit. The function finds the paths
        between the circuits and updates the parameter values for each circuit along the path. It also checks to see
        if the circuit has been visited already, and updates the parameter value if it has. Finally, it returns the
        modified netlist buffer.
        """
        for tuples in self.starting_points:
            path_tuples = self.graph_instance.find_path(tuples[0])
            for edge in path_tuples:
                for component in self.netlist_buffer:
                    if component.typeof == "SubCircuit":
                        if component.visited is False:
                            if component.name == edge[0]:
                                component.parameters += " pipi=kaki"
                                component.visited = True
                        if component.name == edge[0]:
                            for instance in component.instances:
                                if instance.name == edge[1] or instance.parent == edge[1]:
                                    instance.many_parameters["pipi"] = "kaki"
        return self.netlist_buffer

    def generate_netlist(self):
        """
        Generate a netlist from the netlist buffer.

        This function takes a netlist buffer input and produces a netlist file. The netlist file can be used for
        further circuit simulation or design.
        """
        template_loader = jinja2.FileSystemLoader(searchpath="./")
        template_env = jinja2.Environment(loader=template_loader)
        template_file = "templates/subcircuit_template.txt"
        template = template_env.get_template(template_file)
        output = template.render(parsed_netlist=self.propagate_param())
        f = open("netlist/generated_netlist", "w")
        f.write(output)
        f.close()
