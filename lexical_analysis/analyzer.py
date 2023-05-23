import re

class Lexer:
    
    def __init__(self):
        # Define some regular expressions for our lexer
        self.TOKENS = [
            ('INTEGER', r'\d+'),
            ('PLUS', r'\+'),
            ('MINUS', r'\-'),
            ('MULTIPLY', r'\*'),
            ('DIVIDE', r'\/'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
        ]

    # A lexer function that takes a string and returns a list of tokens
    def lexer(self, input_string):
        tokens = []
        while len(input_string) > 0:
            match = None
            for token in TOKENS:
                name, pattern = token
                regex = re.compile(pattern)
                match = regex.match(input_string)
                if match:
                    text = match.group(0)
                    tokens.append((name, text))
                    input_string = input_string[len(text):]
                    break
            if not match:
                raise ValueError(f"Invalid input: {input_string}")
        return tokens
















































































