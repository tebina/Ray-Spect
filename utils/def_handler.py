class DefComponent:
    def __init__(self, typeof):
        self.typeof = typeof

    def __str__(self):
        return str(self.name)

    def __eq__(self, other):
        if isinstance(other, DefComponent):
            return self.name == other.name and self.typeof == other.typeof
        return False

    def __hash__(self):
        return hash((self.typeof, self.name))


class TopInstance(DefComponent):
    def __init__(self, name):
        self.name = name
        DefComponent.__init__(self, 'top_instance')

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __add__(self, other):
        if isinstance(other, str):
            return self.name + other
        else:
            raise TypeError("Unsupported operand type.")


class SubCircuit(DefComponent):
    def __init__(self, name):
        self.name = name
        DefComponent.__init__(self, 'sub_circuit')

    def __repr__(self):
        return self.name

    def __add__(self, other):
        if isinstance(other, str):
            return self.name + other
        else:
            raise TypeError("Unsupported operand type.")


class Instance(DefComponent):
    def __init__(self, name):
        self.name = name
        DefComponent.__init__(self, 'instance')

    def __repr__(self):
        return self.name

    def __add__(self, other):
        if isinstance(other, str):
            return self.name + other
        else:
            raise TypeError("Unsupported operand type.")
