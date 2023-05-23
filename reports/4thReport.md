# Chomsky Normal Form
### Course: Formal Languages & Finite Automata
### Author: Ciumac Alexei FAF-212

---

## Theory

Chomsky Normal Form (CNF) is a standardized representation of a context-free grammar (CFG) that simplifies various computational operations on the grammar. In CNF, all productions have specific forms, either with two non-terminals on the right side or with a single terminal symbol. Additionally, the start symbol does not appear on the right side of any production.

To transform a CFG into CNF, several steps are commonly followed. First, any productions that generate the empty string (epsilon) are removed, except when the start symbol itself can generate epsilon. Next, unit productions (productions with only one non-terminal on the right side) are eliminated. Then, non-terminal symbols appearing in the right side of productions are replaced with pairs of non-terminal symbols, ensuring that each production has at most two non-terminals. Productions of the form A -> a, where 'a' is a terminal symbol, are transformed into two productions: A -> A' and A' -> a, introducing a new non-terminal symbol A'. Finally, a new start symbol S' is introduced along with a production S' -> S, where S is the original start symbol of the grammar.

By following these steps, the resulting grammar will be in CNF. The conversion to CNF is valuable in theoretical computer science and natural language processing as it simplifies the analysis of CFGs and facilitates the use of efficient parsing algorithms.

## Objectives:

1. Learn about Chomsky Normal Form (CNF) [1].
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
   1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
   2. The implemented functionality needs executed and tested.
   3. A BONUS point will be given for the student who will have unit tests that validate the functionality of the project.
   4. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

## Implementation description

In this lab I added a method called _to_cnf_ to **Grammar**

```
def to_cnf(self):
```

**Step 1: Eliminate the start symbol from right-hand sides**

A new start symbol is created by appending a prime (') to the original start symbol until it becomes a unique non-terminal.
The original start symbol is replaced with the new start symbol in the grammar's productions.
```
new_start_symbol = f"{self.start_symbol}'"
while new_start_symbol in self.non_terminals:
    new_start_symbol += "'"
self.productions[new_start_symbol] = [self.start_symbol]
self.start_symbol = new_start_symbol
```

**Step 2: Remove epsilon productions**

Identify the non-terminal symbols that have epsilon (empty string) in their productions and store them in the _epsilon_productions_ set.
Iterate until there are no more epsilon productions:
For each production in the grammar, remove any occurrence of epsilon symbols from the right-hand side by replacing them with an empty string.
Add the modified production back to the grammar.
Update the _epsilon_productions_ set with the non-terminal symbols that still have epsilon in their productions.

```
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
```

**Step 3: Eliminate unit productions**

Create a dictionary, _unit_productions_, to track unit productions for each non-terminal symbol.
Iterate over each symbol and its productions in the grammar:
If a production has only one non-terminal symbol and its length is 1, it is a unit production.
Add the unit production to the corresponding non-terminal symbol's set in _unit_productions_.
While there are unit productions in _unit_productions_:
For each non-terminal symbol and its unit productions:
Remove the unit production from the original symbol's production list.
Add the productions of the unit production to the original symbol's production list.

```
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
```

**Step 4: Introduce new nonterminal symbols for long right-hand sides**

Iterate over each symbol and its productions in the grammar:
If a production has more than two symbols, create a new non-terminal symbol by appending a prime (') and a unique number to the original symbol.
Update the grammar by splitting the long production into two parts:
The last two symbols are assigned to the new non-terminal symbol.
The original symbol's production is modified to exclude the last two symbols and include the new non-terminal symbol.

```
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
```

**Step 5: Eliminate all non-2-sized right-hand sides**

Iterate over each symbol and its productions in the grammar:
Create a new list, _new_productions_, to store the modified productions.
For each production:
If the production has exactly two symbols, add it as is to _new_productions_.
If the production has more than two symbols, split it into pairs of adjacent symbols and create new productions by appending a prime (') to the second symbol of each pair.
Update the grammar's productions for the symbol with the modified _new_productions_.

```
for symbol, productions in self.productions.items():
    new_productions = []
    for production in productions:
        if len(production) == 2:
            new_productions.append(production)
        else:
            new_productions.extend([f"{production[i]}{production[i+1]}'" for i in range(len(production)-1)])
    self.productions[symbol] = new_productions
```

By following these steps, the _to_cnf_ function transforms the original grammar into Chomsky Normal Form (CNF) by applying various transformations and modifications to the productions. The resulting grammar in CNF simplifies computational tasks and enables efficient parsing algorithms.



Drive code to test the functionality of the implemented method:

```
grammar = Grammar(vn, vt, p, ss)

print(" ")
grammar.to_cnf()
print(Grammar(vn, vt, p, ss))
```

## Conclusions / Screenshots / Results

During this laboratory work, I successfully implemented the conversion of a Context-Free Grammar (CFG) to Chomsky Normal Form (CNF), which involved a series of steps. This process allowed me to gain a deeper understanding of CNF and its significance in simplifying grammars for computational tasks. I also learned valuable problem-solving techniques to address challenges encountered during the implementation of the CNF conversion algorithm.

![cnf1](https://github.com/atom-rad/FLFA/assets/113429347/e4663ea3-d86b-4bf7-9de6-081729ce3ac0)

## References
[[1]](https://www.javatpoint.com/automata-chomskys-normal-form)
