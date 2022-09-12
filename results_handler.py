class NetlistElement:
    def __init__(self, typeof):
        self.typeof = typeof

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


class TopInstance(NetlistElement):
    def __init__(self, name, parent, parameters):
        self.name = name
        self.parent = parent
        self.parameters = parameters
        NetlistElement.__init__(self, 'top_instance')

    def __str__(self):
        return self.typeof + " " + self.name + "@" + self.parent + str(self.parameters)

    def __repr__(self):
        return self.name


class BlankLine(NetlistElement):
    def __init__(self, name):
        self.name = name
        NetlistElement.__init__(self, 'blank_line')

    def __str__(self):
        return self.typeof

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


