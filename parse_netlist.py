import pyparsing as pp
import results_handler as rh


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

    identifier = pp.Word(pp.alphanums + '_!<>[]\\')  # a word containing letters and numbers
    expression = pp.Word(pp.alphanums + '._*+-/()')  # any expression, can be a float with negative or an equation
    comment = pp.Group(pp.Keyword("//") + pp.SkipTo(pp.LineEnd())).setResultsName('comment')  # Skipping comments

    # Handling parameters of any type <Var = Value>
    param_name = identifier
    param_value = expression
    inst_parameter = pp.Group(param_name('name') + equal_sign + param_value('value')).setResultsName('key')
    many_parameters = pp.Group(pp.ZeroOrMore(inst_parameter | line_break)).setResultsName(
        'many_parameters')

    # Handling nets
    net = identifier
    nets = pp.Group(pp.OneOrMore(net('net') | line_break))

    # Handling parameter definition line which always starts with "parameters" and ends with a line break
    parameters = pp.Group(pp.Keyword("parameters").suppress() + many_parameters).setResultsName(
        'parameters')

    # Instance handling
    instance_name = identifier
    parent_instance = identifier
    instance = pp.Group(instance_name('name') + open_parenthesis + nets('nets') + close_parenthesis + parent_instance(
        'parent') + many_parameters + eol).setResultsName('instance')

    # Sub-circuit description handling
    subcircuit_name = identifier
    subcircuit_end = pp.Keyword("ends").suppress()  # Circuit end statement
    subcircuit_content = pp.Group(pp.ZeroOrMore(instance | eol)).setResultsName('subnetlist')
    subcircuit = pp.Group(
        # content matches ==> subckt <name> <nets> <eol>
        pp.Keyword("subckt").suppress() + subcircuit_name('name') + nets('nets') + eol
        # content matches the parameters line
        + pp.ZeroOrMore(parameters)
        # content matches ==> parameters_line + instances | instances
        + subcircuit_content
        # content matches ==> ends <name> <eol>
        + subcircuit_end + pp.matchPreviousExpr(subcircuit_name).suppress() + eol).setResultsName('subcircuit')

    # TOP instance is an instance format
    top_instance = instance.setResultsName('top_instance')

    blank_line = eol.setResultsName('blank_line')

    top_instance.setParseAction(handle_top_instances)
    blank_line.setParseAction(handle_blankline)
    subcircuit.setParseAction(handle_subcircuit)
    comment.setParseAction(handle_comments)

    netlist_element = (eol | comment | subcircuit | top_instance | blank_line)
    netlist = pp.ZeroOrMore(netlist_element) + pp.StringEnd()

    return netlist.parseString(file_string)


def handle_subcircuit(token):
    sc = token.subcircuit
    name = sc.name
    instances = sc.subnetlist
    parameters = sc.parameters
    s = rh.SubCircuit(name, instances, parameters)
    return [s]


def handle_top_instances(token):
    sc = token.top_instance
    name = sc.name
    parent = sc.parent
    parameters = sc.parameters
    s = rh.TopInstance(name, parent, parameters)
    return [s]


def handle_blankline(token):
    name = token.blank_line
    s = rh.BlankLine(name)
    return [s]


def handle_comments(token):
    name = token.comment
    s = rh.Comments(name)
    return [s]


def main():
    file = open('netlist/netlist', 'r')
    sample = file.read()
    # parse the netlist
    parsed_netlist = parse_netlist(sample)
    for i in range(len(parsed_netlist)):
        print(parsed_netlist[i])

    # with open('netlist/written_netlist', 'w') as f:
    #     for i in parsed_netlist:
    #         f.write(parsed_netlist[i].__str__())
    # f.close


if __name__ == '__main__':
    main()
