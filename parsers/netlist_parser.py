import pyparsing as pp
from utils import results_handler as rh


def parse_netlist(file_string):
    """
    This function parses a netlist file into a Python list of dictionaries, each containing:
    - A comment
    - A Sub-circuit
    - A TOPLEVEL instance

     The function handles any type of parameter, including those defined on the parameter definition line which
     always starts with "parameters". It also handles instances and sub-circuits. Finally, it prints out the parsed
     netlist.
     :param file_string:
     :return: parsed netlist
    """

    # define a tabulation as a whitespace
    ws = ' \t'
    pp.ParserElement.setDefaultWhitespaceChars(ws)

    # Specter netlist grammar
    eol = pp.lineEnd().suppress()  # End of line
    line_break = pp.Suppress("\\" + pp.LineEnd())  # Line break
    equal_sign = pp.Suppress("=")
    open_parenthesis = pp.Suppress("(")
    close_parenthesis = pp.Suppress(")")

    identifier = pp.Word(pp.alphanums + '._!<>[]\\')  # a word containing letters and numbers
    expression = pp.Word(pp.alphanums + '._*+-/()')  # any expression, can be a float with negative or an equation
    comment = pp.Group(pp.Keyword("//").suppress() + pp.SkipTo(pp.LineEnd())).setResultsName(
        'comment')  # Skipping comments

    # Handling parameters of any type <Var = Value>
    param_name = identifier
    param_value = expression
    inst_parameter = pp.Group(param_name('name') + equal_sign + param_value('value')).setResultsName('key')
    many_parameters = pp.Group(pp.ZeroOrMore(inst_parameter | line_break)).setResultsName(
        'many_parameters')

    # Handling nets
    net = identifier
    nets = pp.Group(pp.OneOrMore(net('net'))).setResultsName('nets')
    # Handling parameter definition line which always starts with "parameters" and ends with a line break
    parameters = pp.Group(pp.Keyword("parameters").suppress() + many_parameters).setResultsName(
        'parameters')

    # Instance handling
    instance_name = identifier
    parent_instance = identifier
    instance = pp.Group(instance_name('name') + open_parenthesis + nets('nets') + close_parenthesis + parent_instance(
        'parent') + many_parameters + eol).setResultsName('instance')
    instance.ignore("\\\n")
    # Sub-circuit description handling
    subcircuit_name = identifier
    subcircuit_end = pp.Keyword("ends").suppress()  # Circuit end statement
    subcircuit_content = pp.Group(pp.ZeroOrMore(instance | eol | line_break)).setResultsName('subnetlist')
    subcircuit = pp.Group(
        # content matches ==> subckt <name> <nets> <eol>
        pp.Keyword("subckt").suppress() + subcircuit_name('name') + nets('pins') + eol
        # content matches the parameters line
        + pp.ZeroOrMore(parameters)
        # content matches ==> parameters_line + instances | instances
        + subcircuit_content
        # content matches ==> ends <name> <eol>
        + subcircuit_end + pp.matchPreviousExpr(subcircuit_name).suppress() + eol).setResultsName('subcircuit')

    # TOP instance is an instance format
    top_instance = instance.setResultsName('top_instance')

    parameters.setParseAction(handle_parameters_line)
    many_parameters.setParseAction(handle_parameters)
    top_instance.setParseAction(handle_top_instances)
    subcircuit.setParseAction(handle_subcircuit)

    netlist_element = (eol | comment | subcircuit | top_instance)
    netlist = pp.ZeroOrMore(netlist_element) + pp.StringEnd()

    return netlist.parseString(file_string)


def handle_subcircuit(token):
    """
    The handle_subcircuit() function takes a token as an argument and returns an instance of the SubCircuit class.
    The SubCircuit class contains information about the subcircuit, including its name, pins, and instances. The
    parameters variable holds the subcircuit's parameters.
    """
    sc = token.subcircuit
    name = sc.name
    instances = sc.subnetlist
    parameters = sc.parameters
    pins = sc.pins
    s = rh.SubCircuit(name, pins, instances, parameters)
    return [s]


def handle_top_instances(token):
    """
    Handle the top instances of a given token.
    Parameters:
    - token (str) - The token to handle.
    - name (str) - The name of the top instance.
    - parent (str) - The parent instance of the top instance.
    - parameters (dict) - The parameters of the top instance.
    - s (TopInstance) - The top instance returned.
    """
    sc = token.top_instance
    name = sc.name
    parent = sc.parent
    nets = sc.nets
    parameters = sc.many_parameters
    s = rh.TopInstance(name, parent, nets, parameters)
    return [s]


def handle_parameters(token):
    """
    transforms the list containing the parameters as tuples into a dictionary {parameter : value , ... }
    :param token:
    :return: dict
    """
    d = {}
    for p in token.many_parameters:
        d[p[0]] = p[1]
    return d


def handle_parameters_line(token):
    """
    Handle parameters on a line

    This function will handle any parameters on a line, and return the text of the parameter as a string.
    :param token
    :return: a long string containing all the parameters in the dict
    """
    d = token.parameters[0]
    t = " ".join(f"{k}={v}" for k, v in d.items())
    return t
