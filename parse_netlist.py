import pyparsing as pp
import results_handler as nl


def parse_netlist(file_string):
    # define a tabulation as a whitespace
    ws = ' \t'
    pp.ParserElement.setDefaultWhitespaceChars(ws)

    # Specter netlist grammar
    eol = pp.lineEnd().suppress()  # End of line
    line_break = pp.Suppress("\\" + pp.LineEnd())  # Line break
    equal_sign = pp.Suppress("=")
    open_parenthesis = pp.Suppress("(")
    close_parenthesis = pp.Suppress(")")

    identifier = pp.Word(pp.alphanums + '_!<>')  # a word containing letters and numbers
    expression = pp.Word(pp.alphanums + '._*+-/()')  # any expression, can be a float with negative or an equation
    comment = pp.Suppress("//" + pp.SkipTo(pp.LineEnd()))  # Skipping comments

    # Handling parameters of any type <Var = Value>
    param_name = identifier
    param_value = expression
    inst_parameter = pp.Group(param_name('name') + equal_sign + param_value('value')).setResultsName('key')
    many_parameters = pp.Group(pp.ZeroOrMore(inst_parameter | line_break)).setResultsName(
        'parameters')

    # Handling nets
    net = identifier
    nets = pp.Group(pp.OneOrMore(net('net') | line_break))

    # Handling parameter definition line which always starts with "parameters" and ends with a line break
    parameter_line = pp.Group(pp.Keyword("parameters").suppress() + many_parameters).setResultsName(
        'line_parameters')

    # Instance handling
    instance_name = identifier
    parent_instance = identifier
    instance = pp.Group(instance_name('name') + open_parenthesis + nets('nets') + close_parenthesis + parent_instance(
        'parent') + many_parameters + eol).setResultsName('instance')

    # Sub-circuit description handling
    subcircuit_name = identifier
    subcircuit_end = pp.Keyword("ends").suppress()  # Circuit end statement
    subcircuit_content = pp.Group(pp.ZeroOrMore(parameter_line | instance | eol)).setResultsName('subnetlist')
    subcircuit = pp.Group(
        # content matches ==> subckt <name> <nets> <eol>
        pp.Keyword("subckt").suppress() + subcircuit_name('name') + nets('nets') + eol
        # content matches ==> parameters_line + instances | instances
        + subcircuit_content
        # content matches ==> ends <name> <eol>
        + subcircuit_end + pp.matchPreviousExpr(subcircuit_name).suppress() + eol).setResultsName('subcircuit')

    #subcircuit.setParseAction(handle_subcircuit)

    netlist_element = (eol | comment | subcircuit)
    netlist = pp.ZeroOrMore(netlist_element) + pp.StringEnd()

    # parameter_line.setParseAction(handle_parameters_line)

    return netlist.parseString(file_string)


def handle_subcircuit(token):
    sc = token.subcircuit
    nets = sc.nets
    name = sc.name
    instances = sc.subnetlist
    s = nl.SubCircuit(name, nets, instances)
    return [s]


file = open('/home/ouldeitn/phd/software/Specrays/string_test', 'r')
sample = file.read()

# parse the netlist
parsed_netlist = parse_netlist(sample)
print(parsed_netlist)


print(parsed_netlist[0].parent)
