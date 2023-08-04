class NetlistElement:
    """
    The NetlistElement class represents a particular type of network element in a
    aes_sbox_netlist. A NetlistElement instance has a type which can be one of
    "SubCircuit", "top_instance", or "comment". It also has a visited property which
    states whether the element has been visited already.
    """

    def __init__(self, typeof):
        """
        Initializes a NetlistElement object.

        Args:
            typeof (str): The type of the NetlistElement.
        """
        self.typeof = typeof
        self.visited = False

    def __str__(self):
        """
        Returns a string representation of the NetlistElement.

        Returns:
            str: The string representation of the NetlistElement.
        """
        return self.typeof

    def __setattr__(self, name, value):
        # Allow modification of all attributes
        self.__dict__[name] = value


class SubCircuit(NetlistElement):
    """
    This class defines a SubCircuit. A SubCircuit is a NetlistElement that represents a circuit with a single input
    and single output. It has a name, instances, and parameters.
    """

    def __init__(self, name, nets, instances, parameters_line):
        """
        Initializes a SubCircuit object.

        Args:
            name (str): The name of the SubCircuit.
            nets (list): The list of nets in the SubCircuit.
            instances (list): The list of instances in the SubCircuit.
            parameters_line (str): The line containing the parameters of the SubCircuit.
        """
        self.name = name
        self.instances = []
        self.parameters = {}
        self.isParameterEmpty = False
        self.nets = nets
        NetlistElement.__init__(self, 'SubCircuit')

        for i in range(len(instances)):
            self.instances.append(Instance(instances[i][0], instances[i][1], instances[i][2],
                                           instances[i][3]))

        for i in range(len(self.nets)):
            self.nets[i] = Pin(self.nets[i], "")

        if parameters_line != '':
            self.isParameterEmpty = True
            for p in parameters_line[0]:
                self.parameters[p[0]] = p[1]

    def __str__(self):
        insts = {}
        for i in self.instances:
            insts[i.name] = i.parent
        return self.typeof + " " + self.name + str(insts)

    def __repr__(self):
        return self.name


class Instance(NetlistElement):
    def __init__(self, name, nets, parent, parameters):
        """
            Initializes an Instance object.

            Args:
                name (str): The name of the Instance.
                nets (list): The list of nets connected to the Instance.
                parent (str): The parent of the Instance.
                parameters (list): The list of parameters of the Instance.
        """
        self.isPmos = False
        self.isNmos = False
        self.name = name
        self.nets = nets
        self.parent = parent
        self.parameters = {}
        NetlistElement.__init__(self, 'instance')

        for i in range(len(self.nets)):
            self.nets[i] = Pin(self.nets[i], self.parent)

        if self.parent == "nsvtgp":
            self.isNmos = True

        if self.parent == "psvtgp":
            self.isPmos = True

        for p in parameters:
            self.parameters[p[0]] = p[1]

    def __str__(self):
        return self.typeof + " " + self.name + "@" + self.parent + str(self.parameters)


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
        self.parameters = {}
        NetlistElement.__init__(self, 'top_instance')
        for i in range(len(self.nets)):
            self.nets[i] = Pin(self.nets[i], self.parent)

        for p in parameters:
            self.parameters[p[0]] = p[1]

    def __str__(self):
        return self.typeof + " " + self.name + "@" + self.parent + str(self.parameters)

    def __repr__(self):
        return self.name


class Pin(NetlistElement):
    def __init__(self, name, parent):
        """
        Initializes a Pin object.

        Args:
            name (str): The name of the Pin.
            parent (str): The parent of the Pin.
        """
        self.name = name
        self.parent = parent
        self.net = False
        self.direction = False
        NetlistElement.__init__(self, 'pin')

    def __repr__(self):
        return self.parent.__repr__() + "." + self.name


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
