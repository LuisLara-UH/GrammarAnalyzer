from Parsers.Utils.FirstFollow import *
from Parsers.LL1 import *
from cmp.utils import *

def Execute_LL1(G):
    text = ""
    
    counter = RemoveLeftRecursive(G)
    RemoveCommonPrefixes(counter, G)

    firsts = compute_firsts(G)
    follows = compute_follows(G, firsts)

    conflict = [(1,1,1), False]
    table = build_parsing_table(G, firsts, follows, conflict)
    firsts[G.EOF] = ContainerSet(G.EOF)
    parser = None 
    nonTerminal , terminal, follow = conflict[0]

    if conflict[1]:
        text += "La Gramatica no es LL1\n"
        text += "Conflicto:\n"
        text += "(" + str(nonTerminal) + "," + str(terminal) + "):" + str(table[nonTerminal, terminal])
        text += "\n"
        form = []
        form.append(G.EOF)
        form.append(G.startSymbol)
        if follow:
            boolean, position = FindNonTerminalWithFollow(form,nonTerminal,{}, terminal, firsts)
        else:
            boolean, position = FindNonTerminal(form,nonTerminal,[])
        
        form1 = []
        for x in form:
            form1.append(x)

        if boolean:
            string, positionx = DoString(form, position, nonTerminal, terminal, table, G, 0)
            text += "Cadena de conflicto:\n"
            for char in string:
                text += str(char)
            text += "\n"
    else:
        text += "La gramatica es LL1.\n"
        text += "Tabla del metodo predictivo no-recursivo:\n"
        for key in table:
            text += str(key) + ":" + str(table[key]) + "\n"
        
        parser = metodo_predictivo_no_recursivo(G, table)
        
        #for cadena in cadenas:
         #   print("Cadena " + str(cadena))
          #  derivation_tree = parser(cadena)
           # if derivation_tree is None:
            #    print("No pertenece al lenguaje")
            #else:
             #   print("Arbol de derivacion:")
              #  pprint(derivation_tree)

    return text, parser