class NetlistElement:
    def __init__(self, typeof):
        self.typeof = typeof
        self.parent = False

    def __str__(self):
        return self.typeof


class SubCircuit(NetlistElement):
    def __init__(self, name, instances, parameters):
        self.name = name
        self.labels = {}
        self.instances = instances
        self.parameters = parameters
        NetlistElement.__init__(self, 'SubCircuit')

    def __str__(self):
        insts = {}
        for i in self.instances:
            insts[i.name] = i.parent
        return self.typeof + " " + self.name + str(insts)

    def map_instances(self, mapping_function):
        for i in range(len(self.instances)):
            self.instances[i] = mapping_function(self.instances[i])

    def __repr__(self):
        return self.name


class Instance(NetlistElement):
    def __init__(self, name, parent, parameters):
        self.name = name
        self.parent = parent
        self.parameters = parameters
        NetlistElement.__init__(self, 'instance')

    def __str__(self):
        return self.typeof + " " + self.name + "@" + self.parent + str(self.parameters)
