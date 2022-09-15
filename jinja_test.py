import jinja2
from parsers.netlist_parser import *

file = open('netlist/netlist', 'r')
sample = file.read()

parsed_netlist = parse_netlist(sample)
# for i in range(len(parsed_netlist)):

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "templates/circuit_template.txt"
template = templateEnv.get_template(TEMPLATE_FILE)

output = template.render(parsed_netlist=parsed_netlist)
print(output)