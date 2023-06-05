class NetlistElement:
    """
    The NetlistElement class represents a particular type of network element in a
    aes_sbox_netlist. A NetlistElement instance has a type which can be one of
    "SubCircuit", "top_instance", or "comment". It also has a visited property which
    states whether the element has been visited already.
    """

    def __init__(self, typeof):
        self.typeof = typeof
        self.visited = False

    def __str__(self):
        return self.typeof



class SubCircuit(NetlistElement):
    """
    This class defines a SubCircuit. A SubCircuit is a NetlistElement that represents a circuit with a single input
    and single output. It has a name, labels, instances, and parameters.
    """

    def __init__(self, name, pins, instances, parameters_line):
        self.name = name
        self.labels = {}
        self.instances = instances
        self.parameters = parameters_line
        self.pins = pins
        NetlistElement.__init__(self, 'SubCircuit')

    def __str__(self):
        insts = {}
        for i in self.instances:
            insts[i.name] = i.parent
        return self.typeof + " " + self.name + str(insts)

    def map_instances(self, mapping_function):
        for i in range(len(self.instances)):
            self.instances[i] = mapping_function(self.instances[i])

    def parameters_check(self):
        if len(self.parameters) != 0:
            return True
        else:
            return False

    def __repr__(self):
        return self.name


class TopInstance(NetlistElement):
    """
    TopInstance is a class that defines the top-level instance of a nets definitions in a NetlistElement. It is
    initialized with the name, parent, and nets of the top-level nets defined in the NetlistElement. The nets and
    parameters can be accessed through the self.nets and self.parameters properties.
    """

    def __init__(self, name, parent, nets, parameters):
        self.name = name
        self.parent = parent
        self.nets = nets
        self.parameters = parameters
        NetlistElement.__init__(self, 'top_instance')

    def __str__(self):
        return self.typeof + " " + self.name + "@" + self.parent + str(self.parameters)

    def __repr__(self):
        return self.name


class Comments(NetlistElement):
    """
    This class defines a comment in a aes_sbox_netlist. Comments are used to document the design of a circuit.
    """

    def __init__(self, name):
        self.name = name
        NetlistElement.__init__(self, 'comment')

    def __str__(self):
        return self.typeof

    def __repr__(self):
        return self.name
