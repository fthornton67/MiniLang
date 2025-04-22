class Block:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"

class Assign:
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def __repr__(self):
        return f"Assign({self.var_name}, {self.value})"

class Declaration:
    def __init__(self, var_type, var_name, value):
        self.var_type = var_type
        self.var_name = var_name
        self.value = value

    def __repr__(self):
        return f"Declaration({self.var_type}, {self.var_name}, {self.value})"

class Print:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Print({self.value})"

class BinaryOp:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.operator}, {self.left}, {self.right})"

class Literal:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Literal({self.value})"

class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"
