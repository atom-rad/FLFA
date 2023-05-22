# Determinism in Finite Automata. Conversion from NDFA 2 DFA. Chomsky Hierarchy.
### Course: Formal Languages & Finite Automata
### Author: Ciumac Alexei FAF-212

---

## Theory

A finite automaton is a mechanism used to model different processes, and its structure is similar to that of a state machine. The term "finite" refers to the fact that an automaton has a starting state and a set of final states, which means that each process modeled by an automaton has a clear beginning and end.

However, there are situations where a single transition can lead to multiple states, which creates a problem known as non-determinism. In the field of systems theory, the degree of determinism in a system is used to measure its predictability. If a system involves random variables, it becomes stochastic or non-deterministic.

Finite automata can be classified as either deterministic or non-deterministic, depending on their structure. It is possible to achieve determinism by following certain algorithms that modify the structure of the automaton. These algorithms can be used to eliminate non-deterministic behavior and improve the predictability of the system.

## Objectives:

1. Understand what an automaton is and what it can be used for.

2. Continuing the work in the same repository and the same project, the following need to be added:
   a. Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.

   b. For this you can use the variant from the previous lab.

3. According to your variant number (by universal convention it is register ID), get the finite automaton definition and do the following tasks:

   a. Implement conversion of a finite automaton to a regular grammar.

   b. Determine whether your FA is deterministic or non-deterministic.

   c. Implement some functionality that would convert an NDFA to a DFA.

   d. Represent the finite automaton graphically (Optional, and can be considered as a **_bonus point_**):

   - You can use external libraries, tools or APIs to generate the figures/diagrams.
   - Your program needs to gather and send the data about the automaton and the lib/tool/API return the visual representation.

## Implementation description


**FiniteAutomaton** class now have a method called _is_deterministic_. This method checks whether the finite automaton is deterministic by examining each state and symbol to ensure that no transition leads to multiple states. If any such transition is found, it returns _False_; otherwise, it returns True.

```
    def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                if len(self.transitions.get((state, symbol), [])) > 1:
                    return False
        return True
```

**_epsilon_closure_** function calculates the epsilon closure of a set of states in the finite automaton. It starts with the given set of states and repeatedly adds any states reachable through epsilon transitions until no more states can be reached. The epsilon closure is returned as a tuple.

```
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
```
**_to_dfa_** method converts the given finite automaton to a deterministic finite automaton (DFA). If the automaton is already deterministic, it returns itself. Otherwise, it begins by obtaining the epsilon closure of the initial state. It then iteratively builds the transitions and states of the resulting DFA by examining each unmarked state and symbol. The algorithm keeps track of visited states to avoid redundant processing. The resulting DFA is returned as an instance of the class.

```
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
```
**Grammar** class now have a method called _chomsky_type_ which returns a string containing information about the Grammar object called it

```
    def chomsky_type(self):
        if all(len(lhs) == 1 and lhs in self.non_terminals for lhs in self.productions.keys()) and all(len(rhs) <= 2 and (rhs[0] in self.terminals or rhs[0] == '') and (len(rhs) == 1 or (len(rhs) == 2 and rhs[1] in self.non_terminals)) for rhs_list in self.productions.values() for rhs in rhs_list):
            return "Type 3 (regular)"

        if all(len(lhs) == 1 and lhs in self.non_terminals for lhs in self.productions.keys()) and all(p in self.non_terminals + self.terminals for rhs_list in self.productions.values() for rhs in rhs_list for p in rhs):
            return "Type 2 (context-free)"

        if all(len(lhs) <= len(rhs) for lhs, rhs_list in self.productions.items() for rhs in rhs_list) and "S" in self.non_terminals and all(p in self.non_terminals + self.terminals for rhs_list in self.productions.values() for rhs in rhs_list for p in rhs):
            return "Type 1 (context-sensitive)"

        if not all(p.isupper() or p == '' for rhs in self.productions.values() for p in rhs):
            return "Type 0 (unrestricted)"

        return "Not a valid Chomsky hierarchy type"
```

As a bonus point I implemented the graphical representation of automatons, using graphviz library.

```
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
```

## Conclusions / Screenshots / Results

In this laboratory work I implemented certain functionality of **Grammar** and **FiniteAutomaton** classes. I learned how can they be transformed each into other. I learned to convert a FA to a DFA and to check grammar's Chomsky Hierarchy type.

## References:
* Hopcroft, John E., and Jeffrey D. Ullman. Introduction to Automata Theory, Languages, and Computation. Addison-Wesley, 1979.
* Sipser, Michael. Introduction to the Theory of Computation. Cengage Learning, 2012.
* "Automata Theory." GeeksforGeeks, https://www.geeksforgeeks.org/automata-theory/.
* "Python | Automata Theory." GeeksforGeeks, https://www.geeksforgeeks.org/python-automata-theory/.
* "Graphviz - Graph Visualization Software." Graphviz, https://graphviz.org/.