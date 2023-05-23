import random

from typing import List
from regular_grammar.finiteAutomaton import FiniteAutomaton



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

    def to_finite_automaton(self):
        states = set(self.non_terminals + ["S"])
        alphabet = set(self.terminals)
        transitions = {}
        initial_state = "S"
        final_states = set()
        iteration = 0
        for symbol in self.non_terminals:
            state1 = symbol
            if iteration > len(self.non_terminals) - 1:
                iteration = 0
            iteration = +1
            state2 = self.non_terminals[iteration]
            if state1 not in transitions:
                transitions[state1] = {}
            for production in self.productions[symbol]:
                if len(production) == 1:
                    transitions[state1][production] = {state2}
                elif len(production) == 2:
                    symbol2 = production[1]
                    if symbol2 not in transitions:
                        transitions[symbol2] = {}
                    transitions[state1][production[0]] = {symbol2}
                    if symbol2 in self.non_terminals:
                        final_states.add(symbol2)
        return FiniteAutomaton(
            states, alphabet, transitions, initial_state, final_states, epsilon_transitions=None
        )
    
    def __str__(self):
        productions_str = "\n".join(self.productions)
        return f"Non-terminals: {self.non_terminals}\nTerminals: {self.terminals}\nProductions:\n{productions_str}\nStart symbol: {self.start_symbol}"

    def is_regular(self):
        for production in self.productions:
            if len(production) > 3:
                return False
            if len(production) == 3 and (
                production[1] not in self.non_terminals
                or production[2] not in self.terminals
            ):
                return False
            if len(production) == 2 and (
                (
                    production[0] not in self.non_terminals
                    and production[0] != self.start_symbol
                )
                or (production[1] not in self.terminals and production[1] != "eps")
            ):
                return False
        return True

    def to_ndfa(self):
        states = set()
        transitions = dict()
        initial_state = "q0"
        final_states = set()

        # Create states
        for i in range(len(self.productions)):
            states.add(f"q{i}")

        # Create transitions
        for production in self.productions:
            if len(production) == 2:
                state1 = (
                    initial_state
                    if production[0] == self.start_symbol
                    else f"q{self.non_terminals.index(production[0])}"
                )
                if state1 not in transitions:
                    transitions[state1] = dict()
                if production[1] != "eps":
                    if production[1] not in transitions[state1]:
                        transitions[state1][production[1]] = set()
                    transitions[state1][production[1]].add(initial_state)
            elif len(production) == 3:
                state1 = (
                    initial_state
                    if production[0] == self.start_symbol
                    else f"q{self.non_terminals.index(production[0])}"
                )
                state2 = f"q{self.non_terminals.index(production[2])}"
                if state1 not in transitions:
                    transitions[state1] = dict()
                if production[1] not in transitions[state1]:
                    transitions[state1][production[1]] = set()
                transitions[state1][production[1]].add(state2)

        # Create final states
        for state in states:
            if "S" in state:
                final_states.add(state)

        return FiniteAutomaton(
            states, self.terminals, transitions, initial_state, final_states
        )
    

    def to_cnf(self):
        # Step 1: eliminate the start symbol from right-hand sides
        new_start_symbol = f"{self.start_symbol}'"
        while new_start_symbol in self.non_terminals:
            new_start_symbol += "'"
        self.productions[new_start_symbol] = [self.start_symbol]
        self.start_symbol = new_start_symbol

        # Step 2: remove epsilon productions
        epsilon_productions = {symbol for symbol, productions in self.productions.items() if "" in productions}
        while epsilon_productions:
            for symbol in self.productions:
                self.productions[symbol] = [
                    production.replace(epsilon_symbol, "")
                    for production in self.productions[symbol]
                    for epsilon_symbol in epsilon_productions
                    if epsilon_symbol in production and (new_production := production.replace(epsilon_symbol, ""))
                ] + self.productions[symbol]
            epsilon_productions = {symbol for symbol, productions in self.productions.items() if "" in productions}
        
        # Step 3: eliminate unit productions
        unit_productions = {symbol: set() for symbol in self.non_terminals}
        for symbol, productions in self.productions.items():
            for production in productions:
                if len(production) == 1 and production in self.non_terminals:
                    symbol=symbol[:-1]
                    print(symbol)
                    print(unit_productions)
                    unit_productions[symbol].add(production)
        while any(unit_productions.values()):
            for symbol, productions in unit_productions.items():
                while productions:
                    production = productions.pop()
                    if production in self.productions[symbol]:
                        self.productions[symbol].remove(production)
                        self.productions[symbol].extend(self.productions[production])
                    
        # Step 4: introduce new nonterminal symbols for long right-hand sides
        new_symbols_counter = 0
        for symbol, productions in self.productions.items():
            for i, production in enumerate(productions):
                if len(production) > 2:
                    new_symbol = f"{symbol}{i+1}'"
                    while new_symbol in self.non_terminals:
                        new_symbol += "'"
                    self.non_terminals.append(new_symbol)
                    self.productions[new_symbol] = [production[-2:]]
                    self.productions[symbol][i] = f"{production[:-2]}{new_symbol}"
        
        # Step 5: eliminate all non-2-sized right-hand sides
        for symbol, productions in self.productions.items():
            new_productions = []
            for production in productions:
                if len(production) == 2:
                    new_productions.append(production)
                else:
                    new_productions.extend([f"{production[i]}{production[i+1]}'" for i in range(len(production)-1)])
            self.productions[symbol] = new_productions


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