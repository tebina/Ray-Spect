
import pyparsing as pp




def parseNetlist(file_string):
    #define a tabular as a whitespace
    ws = ' \t'
    pp.ParserElement.setDefaultWhitespaceChars(ws)

    #Specter netlist grammar
    EOL = pp.lineEnd().suppress() #End of line
    lineBreak = pp.Suppress("\\"+ pp.LineEnd()) #Line break
    identifier = pp.Word(pp.alphanums + '_!<>') # a word containing letters and numbers
    number = pp.Word(pp.nums + ".") #a number, can be float
    expression = pp.Word(pp.alphanums+'._*+-/()')
    comment = pp.Suppress("//" + pp.SkipTo(pp.LineEnd()))#Skipping comments
    net = identifier
    nets = pp.Group(pp.OneOrMore(net('net') | lineBreak)) # many nets
    circuit = identifier  # a net is an identifier
    circuitEnd = pp.Keyword("ends").suppress() #Circuit end statement
    inst_param_key = identifier + pp.Suppress("=")
    inst_param_value = expression('expression')
    inst_parameter = pp.Group(inst_param_key('name') + inst_param_value('value')).setResultsName('key')
    parameters = pp.Group(pp.ZeroOrMore(inst_parameter | lineBreak)).setResultsName('parameters')


    netlist_element = number | identifier | EOL | comment |circuitEnd |expression
    netlist = pp.ZeroOrMore(netlist_element) + pp.StringEnd()

    return netlist.parseString(file_string)


file = open('/home/ouldeitn/phd/software/Specrays/string_test', 'r')
sample = file.read()


# parse the netlist
parsed_netlist = parseNetlist(sample)

# print the top level objects
for obj in parsed_netlist:
    print(obj)

