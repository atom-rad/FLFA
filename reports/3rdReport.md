# Lexer & Scanner
### Course: Formal Languages & Finite Automata
### Author: Ciumac Alexei FAF-212

---

## Theory

The process of extracting lexical tokens from a string of characters is known as lexical analysis, which is commonly referred to as lexer. The term lexer is often used interchangeably with other names, such as tokenizer or scanner. Lexer is an essential component of a compiler/interpreter used in handling programming, markup or other types of languages.

The lexer applies rules of the language to identify tokens from the input stream, which are also called lexemes. Lexemes are produced by splitting the input based on delimiters, such as spaces. In contrast, tokens are assigned categories or names to each lexeme and may contain additional metadata but do not necessarily retain the actual value of the lexeme. The lexer produces a stream of tokens, which distinguishes it from lexemes.

## Objectives:

1. Understand what lexical analysis [1] is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.

## Implementation description

In this lab I added **Lexer** class which contains the dictionary type _TOKENS_. It's assigned as an object of this type is created by constructor.

```
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
```

Attributes

TOKENS: A list of tuples defining the token types and their corresponding regular expression patterns. Each tuple consists of a token name and the regular expression pattern to match.
Methods

lexer(self, input_string): Tokenizes the input string by applying the defined regular expressions. It iteratively matches the patterns against the input string, extracts the matching tokens, and returns a list of token tuples. Each token tuple consists of the token name and the actual text that matches the pattern.

The Lexer class provides an organized and modular approach to perform lexical analysis, separating the tokenization logic into a standalone class. It allows for easy customization and expansion of token definitions by modifying the TOKENS attribute. The lexer() method encapsulates the tokenization process, making it reusable and easily accessible from other parts of the code.

```
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
```

Code for creating a **Lexer** object and lexing a string:

```
lexer = Lexer()  # Create an object of the Lexer class
input_string = input("Enter an arithmetic expression: ")
tokens = lexer.lexer(input_string) # Use the lexer object to call the lexer method
    
# Get the tokens strings
token_strings = [token[1] for token in tokens]
    
# Join the tokens into a single string
token_output = ' '.join(token_strings)
    
# Print the token string
print("The tokens are:", token_output)
```

## Conclusions / Screenshots / Results

In this laboratory work I implemented a lexer. I learned lexing and tokenizing strings.

## References
[1] [A sample of a lexer implementation](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)

[2] [Lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis)