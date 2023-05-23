import graphviz
#import string

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states, epsilon_transitions):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
#        self.inputs = inputs
        self.initial_state = initial_state
        self.final_states = final_states
        self.epsilon_transitions = epsilon_transitions or {}
        self.transition_function = {
    ("q0", "a"): {"q1"},
    ("q1", "b"): {"q2"},
    ("q2", "b"): {"q0"},
    ("q3", "a"): {"q4"},
    ("q4", "a"): {"q0"},
    ("q2", "a"): {"q3"},
    ("q1", "b"): {"q1"},
}
        

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
        print("Current state: ", current_state + " " + str(self.final_states))
        print("Transitions: ", self.transitions)
        return current_state in self.final_states
    

    def to_graphviz(self):
        g = graphviz.Digraph(format="png")
        g.attr(rankdir="LR")

        # Define nodes
        for state in self.states:
            node_attr = {"shape": "circle"}

        for (state, symbol), next_state in self.transition_function.items():
            for target in next_state:
                node_attr = {"shape": "circle"}
                g.node(str(state), **node_attr)
                if str(target) == "q3" and str(state) == "q3":
                    node_attr["peripheries"] = "2"
                    g.node(str(state), **node_attr)
                g.edge(str(state), str(target), label=symbol)

        return g

    def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                if len(self.transitions.get((state, symbol), [])) > 1:
                    return False
        return True

    def epsilon_closure(self, states):
        closure = set(states)
        unprocessed_states = list(states)
        while unprocessed_states:
            state = unprocessed_states.pop()
            for target in self.epsilon_transitions.get(state, []):
                if target not in closure:
                    closure.add(target)
                    unprocessed_states.append(target)
        return tuple(closure)

    def to_dfa(self):
        if self.is_deterministic():
            return self

        initial_state = self.epsilon_closure([self.initial_state])
        transitions = {}
        unmarked_states = [initial_state]
        final_states = []
        alphabet = set(self.alphabet) - {""}
        visited_states = set()  # Add this line

        while unmarked_states:
            # print(unmarked_states)
            current_state = unmarked_states.pop()
            if current_state in visited_states:  # Add this check
                continue
            visited_states.add(current_state)
            for symbol in alphabet:
                next_state = set()
                for state in current_state:
                    next_state |= set(self.transitions.get((state, symbol), []))
                if next_state:
                    next_state_closure = self.epsilon_closure(next_state)
                    transitions[(current_state, symbol)] = next_state_closure
                    if next_state_closure not in unmarked_states:
                        unmarked_states.append(next_state_closure)
                    if any(state in self.final_states for state in next_state_closure):
                        final_states.append(next_state_closure)

        return FiniteAutomaton(
            states={s for t in transitions for s in t[0]} | {s for s in final_states},
            alphabet=self.alphabet,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
            epsilon_transitions=self.epsilon_transitions,
        )

#    def fa2Rg(self):
#        # Define empty set of rules
#        rules = {}
#        counter = 0
#        dictionary = {'q0' : 'S'}
#
#
#        for state in self.states:
#            if(state != 'q0'):
#                dictionary[state] = string.ascii_uppercase[counter]
#                counter += 1
#                
#        # Generate rules for each transition in Delta
#        # for (q, a), next_state in self.transitions.items():
#        for state in self.states:
#            for input in self.inputs:
#                next = self.transitions[state][input]
#                if dictionary[state] not in rules:
#                    rules[dictionary[state]] = []
#                if(next):
#                    rules[dictionary[state]].append(input + (dictionary[next] if dictionary[next] else ''))
#            
#        # Generate the set of non-terminal symbols
#        non_terminal_symbols = list(rules.keys())
#
#        # Generate the dictionary of production rules
#        productions = {}
#        for non_terminal in non_terminal_symbols:
#            productions[non_terminal] = []
#            for production in rules[non_terminal]:
#                productions[non_terminal].append(production)
#                
#            if(non_terminal in [dictionary[item] for item in self.final_states]):
#                productions[non_terminal].append('')
#        
#        
#        # Return the regular grammar
#        return (non_terminal_symbols, self.inputs, productions)