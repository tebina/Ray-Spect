class NetlistElement:
    def __init__(self, typeof):
        self.typeof = typeof
        self.parent = False

    def __str__(self):
        return self.typeof


class SubCircuit(NetlistElement):
    def __init__(self, name, nets, instances):
        self.name = name
        self.labels = {}
        self.power_nets = []
        self.ground_nets = []
        self.internal_nets = []
        # dictionarry of net names,
        # key is net name, value is net object
        # marke these nets also as io
        self.nets = {}  # = nets;
        for n in nets:
            self.nets[n] = Net(n, self)
            self.nets[n].is_io = True

        self.instances = instances
        for i in self.instances:
            # register subcircuit as parrent
            #i.parent = self
            # add all internal nets
            for n in i.pins:
                if n not in self.nets:
                    self.nets[n] = Net(n, self)

        NetlistElement.__init__(self, 'subcircuit')
        print ("subcircuit has been found")

    def __str__(self):
        insts = {}
        for i in self.instances:
            insts[i.name] = i.parent
        return self.typeof + " " + self.name + "(" + str(self.nets) + "):" + str(insts)

    def map_instances(self, mapping_function):
        for i in range(len(self.instances)):
            self.instances[i] = mapping_function(self.instances[i])

    def map_nets(self, mapping_function):
        for n in self.nets:
            self.nets[n] = mapping_function(self.nets[n])

    def __repr__(self):
        return self.name


class Net(NetlistElement):
    def __init__(self, name, parent):
        self.name = name
        self.nettype = 'standard'
        self.nodes = set()
        self.labels = {}
        self.is_vdd = False
        self.is_gnd = False
        self.is_internal = False
        self.is_io = False
        self.parent = parent
        print ("net has been found")

    def connect(self, pin):
        self.nodes.add(pin)

    def __repr__(self):
        return self.parent.__repr__() + "." + self.name


class Instance(NetlistElement):
    def __init__(self, name, pins, parent, parameters):
        self.name = name
        self.pins = pins
        self.parent = parent
        self.parameters = parameters
        NetlistElement.__init__(self, 'instance')
        print ("instance has been found")

    def __str__(self):
        return self.typeof + " " + self.name + "@" + self.parent + str(self.parameters)
