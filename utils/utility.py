import jinja2
import networkx as nx


def netlist_to_dict(parsed_netlist):
    component_dict = {}
    for component in parsed_netlist:
        if component.typeof == "top_instance":
            component_dict["top_instance_" + component.name] = component
        elif component.typeof == "SubCircuit":
            component_dict["sub_circuit_" + component.name] = component
    return component_dict


def generate_netlist(netlist_buffer, generated_netlist_name):
    """
    Generate a aes_sbox_netlist from the aes_sbox_netlist buffer.
    This function takes a aes_sbox_netlist buffer input and produces a aes_sbox_netlist file. The aes_sbox_netlist file can be used for
    further circuit simulation or design.
    """
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "./templates/subcircuit_template"
    template = template_env.get_template(template_file)
    output = template.render(netlist_buffer)
    f = open(generated_netlist_name, "w")
    f.write(output)
    f.close()


def find_path(starting_node, graph_object):
    return list(nx.edge_dfs(graph_object, starting_node))
