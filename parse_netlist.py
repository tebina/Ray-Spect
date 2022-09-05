import pyparsing as pp
ppt = pp.testing


def parse_netlist(file_string):
    # define a tabulation as a whitespace
    ws = ' \t'
    pp.ParserElement.setDefaultWhitespaceChars(ws)

    # Specter netlist grammar
    eol = pp.lineEnd().suppress()  # End of line
    line_break = pp.Suppress("\\" + pp.LineEnd())  # Line break
    equal_sign = pp.Suppress("=")
    circuit_end = pp.Keyword("ends").suppress()  # Circuit end statement
    identifier = pp.Word(pp.alphanums + '_!<>') # a word containing letters and numbers
    expression = pp.Word(pp.alphanums+'._*+-/()') # any expression, can be a float with negative or an equation
    comment = pp.Suppress("//" + pp.SkipTo(pp.LineEnd()))  # Skipping comments

    # Handling parameters of any type <Var = Value>
    inst_param_name = identifier
    inst_param_value = expression
    inst_parameter = pp.Group(inst_param_name('name') + equal_sign + inst_param_value('value')).setResultsName('key').set_debug()

    # Handling parameter definition line which always starts with "parameters" and ends with a line break
    parameter_line = pp.Group('parameters' + pp.ZeroOrMore(inst_parameter | line_break)).setResultsName('parameters_line')



    netlist_element = (eol | comment | circuit_end | inst_parameter | parameter_line)
    print(ppt.with_line_numbers(file_string))

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
