from utils.generate_graph import GenerateGraph
from parsers.netlist_parser import parse_netlist

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

    def prepare_edges(self):
        for tuples in self.starting_points:
            path_tuples = self.graph_instance.find_path(tuples[0])
            print(path_tuples)

    def propagate_param(self):
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
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        TEMPLATE_FILE = "templates/subcircuit_template.txt"
        template = templateEnv.get_template(TEMPLATE_FILE)
        output = template.render(parsed_netlist=self.propagate_param())
        f = open("generated_netlist", "w")
        f.write(output)
        f.close()
