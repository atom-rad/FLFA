from analyzer import Lexer
from parser import Parser
from AST import Identifier, Operator, Integer, String, VariableDeclaration

import os


def main():

    with open('src_code.txt', 'r') as file:
        src_code = file.read()
    lex = Lexer(src_code)

    tokens = lex.tokenize()
    pars = Parser(tokens)
    ast_nodes = pars.parse()

    # Print the AST nodes
    for node in ast_nodes:
        print(node.__class__.__name__)
        if isinstance(node, VariableDeclaration):
            print("Identifier:", node.identifier.value)
            if isinstance(node.value, Integer):
                print("Value (Integer):", node.value.value)
            elif isinstance(node.value, String):
                print("Value (String):", node.value.value)


if "__name__" == main():
    main()