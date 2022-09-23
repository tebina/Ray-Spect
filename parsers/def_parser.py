import pyparsing as pp


def parse_def(file_string):
    # define a tabulation as a whitespace
    ws = ' \t'
    pp.ParserElement.setDefaultWhitespaceChars(ws)

    # def file grammar
    eol = pp.lineEnd().suppress()  # End of line
    plus_sign = pp.Suppress("+")
    minus_sign = pp.Suppress("-")
    line_end = pp.Suppress(";" + pp.LineEnd())
    open_parenthesis = pp.Suppress("(")
    close_parenthesis = pp.Suppress(")")

    identifier = pp.Word(pp.alphanums + '_!<>[]\\')
    separator_slash = pp.Suppress("/")

    number = pp.Word(pp.nums)

    weight_expression = pp.Suppress("WEIGHT")
    component_number = number

    components_start = pp.Keyword("COMPONENTS").suppress() + component_number + line_end
    components_end = pp.Keyword("END COMPONENTS").suppress()

    component_type = pp.OneOrMore(identifier)
    component_state = identifier
    component_parent = identifier
    component_coordinates = pp.OneOrMore(number).setResultsName('coordinates')
    orientation = identifier
    weight = number

    component_path = pp.Group(pp.OneOrMore(identifier | separator_slash)).setResultsName('name')

    component_definition = pp.Group(minus_sign + component_path + plus_sign + pp.Group(pp.ZeroOrMore(
        component_type + plus_sign)) + component_state + open_parenthesis + component_coordinates + close_parenthesis +
                                    orientation + pp.Group(pp.ZeroOrMore(plus_sign + weight_expression + weight) | eol))

    all_components = pp.Group(
        components_start + pp.OneOrMore(component_definition | line_end) + components_end
    )
    txt = pp.SkipTo(component_definition) | pp.SkipTo(pp.StringEnd(), include=True)

    components = pp.ZeroOrMore(component_definition | pp.Suppress(txt))

    return components.parseString(file_string)


file = open('../netlist/sboxTOP.def', 'r')
sample = file.read()
parsed_def = parse_def(sample)

f = open("components", "w")
f.write(str(parsed_def[1]))
f.close()
