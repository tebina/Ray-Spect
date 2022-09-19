class NetlistElement:
    def __init__(self, typeof):
        self.typeof = typeof

    def __str__(self):
        return self.typeof


class SubCircuit(NetlistElement):
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
    def __init__(self, name):
        self.name = name
        NetlistElement.__init__(self, 'comment')

    def __str__(self):
        return self.typeof

    def __repr__(self):
        return self.name
