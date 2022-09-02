import pyparsing as pp


def parse_netlist(file_string):
    # define a tabulation as a whitespace
    ws = ' \t'
    pp.ParserElement.setDefaultWhitespaceChars(ws)

    # Specter netlist grammar
    eol = pp.lineEnd().suppress()  # End of line
    line_break = pp.Suppress("\\" + pp.LineEnd())  # Line break
    identifier = pp.Word(pp.alphanums + '_!<>')  # a word containing letters and numbers
    number = pp.Word(pp.nums + ".ue-")  # a number, can be float
    expression = pp.Word(pp.alphanums + '._*+-/()')
    comment = pp.Suppress("//" + pp.SkipTo(pp.LineEnd()))  # Skipping comments
    net = identifier
    nets = pp.Group(pp.OneOrMore(net('net') | line_break))  # many nets
    circuit = identifier  # a net is an identifier
    circuit_end = pp.Keyword("ends").suppress()  # Circuit end statement
    inst_param_name = expression

    inst_param_value = pp.Suppress("=") + number  # value of a param, can contain exp and negative exp and the unit
    inst_parameter = pp.Group(inst_param_name('name') + inst_param_value('value')).setResultsName('key')
    parameters = pp.Group(pp.ZeroOrMore(inst_parameter | line_break)).setResultsName('parameters')

    netlist_element = number | identifier | eol | comment | circuit_end | parameters | expression
    netlist = pp.ZeroOrMore(netlist_element) + pp.StringEnd()

    return netlist.parseString(file_string)


file = open('/home/ouldeitn/phd/software/Specrays/string_test', 'r')
sample = file.read()

# parse the netlist
parsed_netlist = parse_netlist(sample)
print(parsed_netlist)
# print the top level objects
# for obj in parsed_netlist:
#     print(obj)
