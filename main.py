from src.generate_graph import GenerateGraph
from src.model_xray import ModelXray
from utils.utility import generate_netlist

netlist_graph = GenerateGraph("st_netlist",
                              "st_netlist.def", (0, 0), (20, 20))
netlist_graph.plot_region()
#netlist_graph.plot_graph()
model = ModelXray(netlist_graph,0,0.8,0.1)
model.propagate_model()
model.generate_netlist("generated_netlist")
#netlist_buffer = PropagateParam(netlist_graph, "vthadd", 0.02).propagate_param()
#netlist_obj = mx(parsed_netlist, parsed_def, 1,1).generate_netlist("generated_netlist")
# netlist_obj.generate_netlist("generated_netlist")


