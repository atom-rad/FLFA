from AST import Identifier, Operator, Integer, String, VariableDeclaration


class Parser(object):
    def __init__(self, tokens):
        self.tokens = tokens  # Store the list of tokens received from the lexer
        self.token_index = 0  # Initialize the token index to the first token

    # Main function to parse the tokens and build the AST
    def parse(self):
        ast_nodes = []  # List to store the generated AST nodes

        # Iterate through the tokens while there are more tokens to process
        while self.token_index < len(self.tokens):
            token_type = self.tokens[self.token_index][0]
            token_value = self.tokens[self.token_index][1]

            # If the token is a variable declaration
            if token_type == 'DECLARATION' and token_value == 'var':
                # Call the parse_var_declaration function and add the returned node to the ast_nodes list
                var_decl_node = self.parse_var_declaration(self.tokens[self.token_index:len(self.tokens)])
                ast_nodes.append(var_decl_node)

            # Increment the token index to move on to the next token
            self.token_index += 1

        # Return the list of AST nodes
        return ast_nodes

    # Function to parse a variable declaration and create an AST node for it
    def parse_var_declaration(self, tokens):
        tokens_verified = 0
        identifier = None
        operator = None
        value = None

        # Iterate through the tokens in the variable declaration
        for token in range(0, len(tokens)):
            token_type = tokens[tokens_verified][0]
            token_value = tokens[tokens_verified][1]

            # Ignore the variable type (e.g., "var") token, since it's not needed in the AST
            if token == 0:
                pass

            # Process the identifier (variable name) token
            elif token == 1 and token_type == 'IDENTIFIER':
                identifier = Identifier(token_value)
            elif token == 1 and token_type != 'IDENTIFIER':
                raise ValueError('Error: Invalid variable name: ' + token_value)

            # Process the operator (assignment) token
            elif token == 2 and token_type == 'OPERATOR':
                operator = Operator(token_value)
            elif token == 2 and token_type != 'OPERATOR':
                raise ValueError('Error: Invalid assign operator ')

            # Process the value (assigned to the variable) token
            elif token == 3 and token_type in ['IDENTIFIER', 'INTEGER', 'STRING']:
                if token_type == 'INTEGER':
                    value = Integer(token_value)
                elif token_type == 'IDENTIFIER':
                    value = Identifier(token_value)
                elif token_type == 'STRING':
                    value = String(token_value)

            # Ignore the separator (e.g., ";") token, since it's not needed in the AST
            elif token == 4 and token_type == 'SEPARATOR':
                pass

            # Increment the tokens_verified counter to move on to the next token
            tokens_verified += 1

        # Create a new VariableDeclaration AST node with the identifier and value
        variable_declaration = VariableDeclaration(identifier, value)
        # Update the token_index by the number of tokens verified in this variable declaration
        self.token_index += tokens_verified

        # Return the created VariableDeclaration AST node
        return variable_declaration