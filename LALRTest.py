from Parsers.LALR import *
from cmp.pycompiler import Grammar
from Parsers.Utils.FirstFollow import *
from Parsers.Utils.ShiftReduceUtils import *
from GrammarOperations import *

def Execute_LALR(G):
    text = ""

    parser = LALRParser(G)
    conflicts = parser.conflicts    
    automaton = parser.automaton

    if len(conflicts) == 0:
        text += "No hay conflictos\n"
        text += "Action:\n"
        for key in parser.action:
            text += "(" + str(key) + "):" + str(parser.action[key]) + "\n"
        text += "Goto:\n"
        for key in parser.goto:
            text += "(" + str(key) + "):" + str(parser.goto[key]) + "\n"
    else:
        text += "Conflicto:\n"
        text += str(conflicts[0]) + "\n"
        terminal, node = conflicts[0]
        
        for action in parser.action[node.idx, terminal]:
            if action[0] == "REDUCE":
                reduce_item_conflict = action[1]
                break
        
        items_conflict_way = FindStart(automaton, node, Item(reduce_item_conflict, len(reduce_item_conflict.Right)))
        items_to_conflict_way = FindConflict(Item(parser.G.startSymbol.productions[0], 0), automaton, items_conflict_way[0])
        
        items_to_expand = items_to_conflict_way + items_conflict_way
        print(items_to_expand)

        conflict_string = FindConflictString(items_to_expand)

        if not conflict_string is None:
            text += "Cadena de conflicto:\n"
            for char in conflict_string:
                text += str(char)
            text += "\n"
        
    return text, automaton, parser

G = Grammar()

S = G.NonTerminal('A', True)
E, T, F = G.NonTerminals('E T F')
plus, opar, cpar, mul, n = G.Terminals('+ ( ) * n')

S %= E
E %= T | E + plus + T
T %= F | T + mul + F
F %= n | opar + E + cpar

text, automaton, parser = Execute_LALR(G)

#automata = Derivation_Tree_ShiftReduce(parser, [a, b, G.EOF])

