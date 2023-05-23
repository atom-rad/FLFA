from regular_grammar.finiteAutomaton import FiniteAutomaton
from regular_grammar.grammar import Grammar
from lexical_analysis.analyzer import Lexer

# def main():
vn = ["S", "D", "E", "J"]
vt = ["a", "b", "c", "d", "e"]
p = {
    "S": ["aD"],
    "D": ["dE", "bJ", "aE"],
    "E": ["e", "aE"],
    "J": ["cS"]
}
ss = "S"

grammar = Grammar(vn, vt, p, ss)


# Generate a string
input_array = []
while len(input_array) < 5:
    input_string = grammar.generate_string()
    if input_string not in input_array:
        input_array.append(input_string)


finite_automaton = grammar.to_finite_automaton()

# Test if the string matches the rules
for i in range(len(input_array)):
    print(input_array[i])
    if finite_automaton.string_belongs_to_language(input_array[i]):
        print("String", input_array[i], "matches the grammar rules")
        print(" ")
    else:
        print("String", input_array[i], "does not match the grammar rules")
        print(" ")

states = {"q0", "q1", "q2", "q3", "q4"}
alphabet = {"a", "b"}
transition_function = {
    ("q0", "a"): {"q1"},
    ("q1", "b"): {"q2"},
    ("q2", "b"): {"q0"},
    ("q3", "a"): {"q4"},
    ("q4", "a"): {"q0"},
    ("q1", "b"): {"q1"},
    ("q2", "a"): {"q3"}
}

epsilon_transitions = None,

# Define the initial and final states
initial_state = "q0"
final_states = {"q3"}

# Create the finite automaton
fa = FiniteAutomaton(
    states, alphabet, transition_function, initial_state, final_states, epsilon_transitions=None
)

# Test the methods
print(fa.is_deterministic(), "that FA is deterministic")
print(grammar.chomsky_type())
dfa = fa.to_dfa()
g = dfa.to_graphviz()
g.render("dfa")

print(" ")
grammar.to_cnf()
print(Grammar(vn, vt, p, ss))

lexer = Lexer()  # Create an object of the Lexer class
input_string = input("Enter an arithmetic expression: ")
tokens = lexer.lexer(input_string) # Use the lexer object to call the lexer method
    
# Get the tokens strings
token_strings = [token[1] for token in tokens]
    
# Join the tokens into a single string
token_output = ' '.join(token_strings)
    
# Print the token string
print("The tokens are:", token_output)


