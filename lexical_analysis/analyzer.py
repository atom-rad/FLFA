import re


class Lexer:
    def __init__(self, src_code):
        self.src_code = src_code

    def tokenize(self):
        # This list will keep all tokens
        tokens = []

        # Splitting the source code into "tokens"
        src_code = self.src_code.split()

        t_index = 0

        # Iterating through "tokens" and dividing into categories
        while t_index < len(src_code):
            token = src_code[t_index]

            # Recognise variable declaration
            if token == "var":
                tokens.append(['DECLARATION', token])

            # Recognise an integer
            elif re.match('[0-9]', token):
                if token[-1] == ";":
                    tokens.append(['INTEGER', token[:-1]])
                else:
                    tokens.append(['INTEGER', token])

            # Recognise a word
            elif re.match('[a-z]', token) or re.match('[A-Z]', token):
                if token[-1] == ";":
                    tokens.append(['IDENTIFIER', token[:-1]])
                else:
                    tokens.append(['IDENTIFIER', token])

            # Recognise an operation
            elif token in "+-=/*":
                tokens.append(['OPERATOR', token])

            # Recognise the separator, for this case also end of declaration
            if token[-1] == ";":
                tokens.append(['SEPARATOR', token[-1]])

            t_index += 1
        return tokens

