# Intro to formal languages. Regular grammars. Finite Automata.
### Course: Formal Languages & Finite Automata
### Author: Ciumac Alexei FAF-212

---

## Theory

A finite automaton is a mechanism used to model different processes, and its structure is similar to that of a state machine. The term "finite" refers to the fact that an automaton has a starting state and a set of final states, which means that each process modeled by an automaton has a clear beginning and end.

However, there are situations where a single transition can lead to multiple states, which creates a problem known as non-determinism. In the field of systems theory, the degree of determinism in a system is used to measure its predictability. If a system involves random variables, it becomes stochastic or non-deterministic.

Finite automata can be classified as either deterministic or non-deterministic, depending on their structure. It is possible to achieve determinism by following certain algorithms that modify the structure of the automaton. These algorithms can be used to eliminate non-deterministic behavior and improve the predictability of the system.

## Objectives:

* Understand what a language is and what it needs to have in order to be considered a formal one.

* Provide the initial setup for the evolving project that you will work on during this semester. I said project because usually at lab works, I encourage/impose students to treat all the labs like stages of development of a whole project. Basically you need to do the following:

  a. Create a local && remote repository of a VCS hosting service (let us all use Github to avoid unnecessary headaches);

  b. Choose a programming language, and my suggestion would be to choose one that supports all the main paradigms;

  c. Create a separate folder where you will be keeping the report. This semester I wish I won't see reports alongside source code files, fingers crossed;

* According to your variant number (by universal convention it is register ID), get the grammar definition and do the following tasks:

  a. Implement a type/class for your grammar;

  b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

  c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;

  d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;

## Implementation description

I created two classes named **Grammar** and **FiniteAutomaton**.
**Grammar** class has a constructor assigning object's attributes(non_terminals, terminals, productions and start_symbol) to the given values at the initialization

```
class Grammar:
    def __init__(
        self,
        non_terminals: List[str],
        terminals: List[str],
        productions: List[str],
        start_symbol: str,
    ):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol
```
and a method, called _generate_string_, which generates a string picking random transitions.
```
    def generate_string(self):
        string = ""
        stack = [self.start_symbol]
        while stack:
            symbol = stack.pop()
            if symbol in self.terminals:
                string += symbol
            else:
                productions = self.productions[symbol]
                chosen_production = random.choice(productions)
                for s in reversed(chosen_production):
                    stack.append(s)
        return string
```

**FiniteAutomaton** class also has a constructor assigning its attributes.
```
class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
```

This method, called _string_belongs_to_language_, receives any string and checks if it corresponds to given grammar step-by-state.
```
    def string_belongs_to_language(self, input_string):
        if input_string[len(input_string) - 1] == "a":
            # print("ends with 'a'")
            return False
        current_state = self.initial_state

        for symbol in input_string:
            if symbol not in self.alphabet:
                print("not in alphabet")
                return False
            if current_state not in self.transitions:
                print("not in TRANSITIONS")
                return False
            if symbol not in self.transitions[current_state]:
                return False
            current_state = next(iter(self.transitions[current_state][symbol]))
            print(current_state)
        print(current_state + " " + str(self.final_states))
        print(self.transitions)
        return current_state in self.final_states
```

**Main** file takes given data
```
from regular_grammar.finiteAutomaton import FiniteAutomaton
from regular_grammar.grammar import Grammar

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
```
and makes **Grammar** object
```
grammar = Grammar(vn, vt, p, ss)
```
and runs _generate_string_ method five times, printing returned string alongside with an approval or disproval of belonging this string to given language, basing on returned value of _string_belongs_to_language_ method, called with this string as an argument.
```
input_array = []
while len(input_array) < 5:
    input_string = grammar.generate_string()
    if input_string not in input_array:
        input_array.append(input_string)

finite_automaton = grammar.to_finite_automaton()

for i in range(len(input_array)):
    print(input_array[i])
    if finite_automaton.string_belongs_to_language(input_array[i]):
        print("String", input_string, "matches the grammar rules")
    else:
        print("String", input_string, "does not match the grammar rules")
```
Here's some code results:
```
aae
D
E
D
D {'S', 'J', 'D', 'E'}
{'S': {'a': {'D'}}, 'D': {'d': {'E'}, 'b': {'J'}, 'a': {'E'}}, 'E': {'e': {'D'}, 'a': {'E'}}, 'J': {'c': {'S'}}}
String abcabcadae matches the grammar rules
aaae
D
E
E
D
D {'S', 'J', 'D', 'E'}
{'S': {'a': {'D'}}, 'D': {'d': {'E'}, 'b': {'J'}, 'a': {'E'}}, 'E': {'e': {'D'}, 'a': {'E'}}, 'J': {'c': {'S'}}}
String abcabcadae matches the grammar rules
abcadaae
D
J
S
D
E
E
E
D
D {'S', 'J', 'D', 'E'}
{'S': {'a': {'D'}}, 'D': {'d': {'E'}, 'b': {'J'}, 'a': {'E'}}, 'E': {'e': {'D'}, 'a': {'E'}}, 'J': {'c': {'S'}}}
String abcabcadae matches the grammar rules
ade
D
E
D
D {'S', 'J', 'D', 'E'}
{'S': {'a': {'D'}}, 'D': {'d': {'E'}, 'b': {'J'}, 'a': {'E'}}, 'E': {'e': {'D'}, 'a': {'E'}}, 'J': {'c': {'S'}}}
String abcabcadae matches the grammar rules
abcabcadae
D
J
S
D
J
S
D
E
E
D
D {'S', 'J', 'D', 'E'}
{'S': {'a': {'D'}}, 'D': {'d': {'E'}, 'b': {'J'}, 'a': {'E'}}, 'E': {'e': {'D'}, 'a': {'E'}}, 'J': {'c': {'S'}}}
String abcabcadae matches the grammar rules
True
```
```
aaaaae
D
E
E
E
E
D
D {'S', 'J', 'E', 'D'}
{'S': {'a': {'D'}}, 'D': {'d': {'E'}, 'b': {'J'}, 'a': {'E'}}, 'E': {'e': {'D'}, 'a': {'E'}}, 'J': {'c': {'S'}}}
String abcabcaaaae matches the grammar rules
adae
D
E
E
D
D {'S', 'J', 'E', 'D'}
{'S': {'a': {'D'}}, 'D': {'d': {'E'}, 'b': {'J'}, 'a': {'E'}}, 'E': {'e': {'D'}, 'a': {'E'}}, 'J': {'c': {'S'}}}
String abcabcaaaae matches the grammar rules
aaae
D
E
E
D
D {'S', 'J', 'E', 'D'}
{'S': {'a': {'D'}}, 'D': {'d': {'E'}, 'b': {'J'}, 'a': {'E'}}, 'E': {'e': {'D'}, 'a': {'E'}}, 'J': {'c': {'S'}}}
String abcabcaaaae matches the grammar rules
ade
D
E
D
D {'S', 'J', 'E', 'D'}
{'S': {'a': {'D'}}, 'D': {'d': {'E'}, 'b': {'J'}, 'a': {'E'}}, 'E': {'e': {'D'}, 'a': {'E'}}, 'J': {'c': {'S'}}}
String abcabcaaaae matches the grammar rules
abcabcaaaae
D
J
S
D
J
S
D
E
E
E
D
D {'S', 'J', 'E', 'D'}
{'S': {'a': {'D'}}, 'D': {'d': {'E'}, 'b': {'J'}, 'a': {'E'}}, 'E': {'e': {'D'}, 'a': {'E'}}, 'J': {'c': {'S'}}}
String abcabcaaaae matches the grammar rules
True
```

## Conclusions
In this laboratory work I implemented the concept of regular grammar and finite automaton. I learned how they work and their relationship with each other. I learned to convert a regular grammar to a finite automaton and check the corresponding strings through it.



## References
* Introduction to Finite Automata - https://www.geeksforgeeks.org/introduction-of-finite-automata/
* Deterministic Finite Automata - https://www.geeksforgeeks.org/deterministic-finite-automata-acceptance-of-strings/
* Non-Deterministic Finite Automata - https://www.geeksforgeeks.org/nondeterministic-finite-automata-nfa/
* Pushdown Automata - https://www.geeksforgeeks.org/pushdown-automata-introduction/
* Turing Machine - https://www.geeksforgeeks.org/turing-machine-introduction/
* Mealy and Moore Machines - https://www.geeksforgeeks.org/mealy-and-moore-machines/