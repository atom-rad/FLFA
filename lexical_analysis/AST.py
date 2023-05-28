# Base class for all nodes in the AST
class Node:
    pass


# Class representing a variable declaration in the AST
class VariableDeclaration(Node):
    def __init__(self, identifier, value):
        self.identifier = identifier  # Identifier node representing the variable name
        self.value = value  # Value node representing the initial value assigned to the variable


# Class representing an assignment statement in the AST
class Assignment(Node):
    def __init__(self, identifier, operator, value):
        self.identifier = identifier  # Identifier node representing the variable name
        self.operator = operator  # Operator node representing the assignment operator
        self.value = value  # Value node representing the value assigned to the variable


# Class representing an identifier (variable name) in the AST
class Identifier(Node):
    def __init__(self, value):
        self.value = value  # String representing the identifier


# Class representing an integer value in the AST
class Integer(Node):
    def __init__(self, value):
        self.value = value  # Integer value


# Class representing a string value in the AST
class String(Node):
    def __init__(self, value):
        self.value = value  # String value


# Class representing an operator (e.g., assignment) in the AST
class Operator(Node):
    def __init__(self, value):
        self.value = value  # String representing the operator