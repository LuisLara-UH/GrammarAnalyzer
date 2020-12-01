from Parsers.Utils.FirstFollow import *
from Parsers.LL1 import *
from Parsers.Utils.RegularGrammar import *
from cmp.automata import *

def Execute(G):
    text = ""

    firsts = compute_firsts(G)
    follows = compute_follows(G, firsts)

    text += "Firsts:\n"
    for key in firsts:
        text += str(key) + ":" + str(firsts[key]) + "\n"
    
    text += "\n"
    text += "Follows:\n"
    for key in follows:
        text += str(key) + ":" + str(follows[key]) + "\n"
    text += "\n"

    is_regular = IsRegular(G)
    automata = None
    if is_regular:
        text += "La gramatica es regular.\n"
        automata = ToAutomata(G.nonTerminals)
        regular_expression = ToRegularExpression(automata)
        text += "Expresion Regular: " + str(regular_expression) + "\n\n"
    else:
        text += "La gramatica no es regular.\n\n"

    text += "Gramatica sin recursion izquierda inmediata ni prefijos comunes:\n"
     
    counter = RemoveLeftRecursive(G)
    print(G)
    RemoveCommonPrefixes(counter, G)
    text += str(G) + "\n"

    return text, automata

def Derivation_Tree(parser, string):
    derivation_tree = parser(string)

    if derivation_tree is None:
        return None

    start = State(derivation_tree[0].Left.Name)
    symbol_state = {}
    symbol_state[derivation_tree[0].Left.Name] = [start]

    for production in derivation_tree:
        left = production.Left
        right = production.Right

        from_state = symbol_state[left.Name].pop()

        i = len(right) - 1
        while i >= 0:
            new_state = State(right[i].Name)

            try:
                symbol_state[right[i].Name].append(new_state)
            except KeyError:
                symbol_state[right[i].Name] = [new_state]
            i -= 1

            from_state.add_transition('', new_state)

    return start

def Derivation_Tree_ShiftReduce(parser, string):
    derivation_tree = parser.__call__(string)
    
    if derivation_tree is None:
        return None

    start = State(derivation_tree[0].Left.Name)
    symbol_state = {}
    symbol_state[derivation_tree[0].Left.Name] = [start]

    for production in derivation_tree:
        left = production.Left
        right = production.Right

        from_state = symbol_state[left.Name].pop()

        if right.IsEpsilon:
            new_state = State('e')
            from_state.add_transition('', new_state)
        
        else:
            i = len(right) - 1
            while i >= 0:
                new_state = State(right[i].Name)

                try:
                    symbol_state[right[i].Name].append(new_state)
                except KeyError:
                    symbol_state[right[i].Name] = [new_state]
                i -= 1

                from_state.add_transition('', new_state)

    return start

