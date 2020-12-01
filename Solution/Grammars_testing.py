from LL1Test import Execute_LL1
from SLR1ParserTest import Execute_SLR1
from LR1Test import Execute_LR1
from LALRTest import Execute_LALR
from cmp.pycompiler import Grammar

def G1():
    G = Grammar()

    A = G.NonTerminal('A', True)
    B, C, D = G.NonTerminals('B C D')
    a, b, c, d = G.Terminals('a b c d')

    A %= a + B
    B %= b

    return G

def G2():
    G = Grammar()

    S = G.NonTerminal('A', True)
    E, T, F = G.NonTerminals('E T F')
    plus, opar, cpar, mul, n = G.Terminals('+ ( ) * n')

    S %= E
    E %= T | E + plus + T
    T %= F | T + mul + F
    F %= n | opar + E + cpar

    return G

#-------    LL1     -------
def G3():
    G = Grammar()
    S = G.NonTerminal('S', True)
    F = G.NonTerminal('F')
    a, plus, opar, cpar = G.Terminals('a + ( )')

    S %= F
    S %= opar + S + plus + F + cpar
    F %= a

    return G

#------LR0--------
def G4():
    G = Grammar()
    E = G.NonTerminal('E', True)
    B = G.NonTerminal('B')
    cero, one, plus, star = G.Terminals('0 1 + *')

    E %= E + star + B
    E %= E + plus + B
    E %= B
    B %= cero
    B %= one

    return G

 #LL(1) not SLR(1)
 #S -> AaAb | BbBa
 #A -> epsilon
 #B -> epsilon

def G5():
    G = Grammar()
    S = G.NonTerminal('S', True)
    A = G.NonTerminal('A')
    a = G.Terminal('a')

    S %= S + A | A
    A %= a

    return G

#LALR(1) not SLR(1)
def G6():
    G = Grammar()
    S = G.NonTerminal('S', True)
    A = G.NonTerminal('A')
    a, b, c, d = G.Terminals('a b c d')

    S %= A + a | b + A + c | d + c | b + d + a
    A %= d

    return G

#LR(1) not LALR(1)
def G7():
    G = Grammar()
    S = G.NonTerminal('S', True)
    A, B = G.NonTerminals('A B')
    a, b, c, d = G.Terminals('a b c d')

    S %= A + a | b + A + c | B + c | b + B + a
    A %= d
    B %= d

    return G

def G8():
    G = Grammar()
    A = G.NonTerminal('A', True)
    B, C = G.NonTerminals('B C')
    x, y, z = G.Terminals('x y z')

    A %= C + x + A | G.Epsilon
    B %= x + C + y | x + C
    C %= x + B + x | z

    return G

# bfs(tree)
def G9():
    G = Grammar()
    E = G.NonTerminal('E', True)
    T, F = G.NonTerminals('T F')
    num, plus, star, opar, cpar = G.Terminals('n + * ( )')

    E %= E + plus +  T | T
    T %= T + star + F | F
    F %= num | opar + E + cpar

    return G

#functions = [ G1, G2, G3, G4, G5, G6, G7, G8, G9 ]
functions = [ G7 ]

for function in functions:
    G = function()
    print("Gramatica:")
    print(G)
    print()

    print("Parser LL1")
    text, parser = Execute_LL1(G)
    print(text)
    print()

    print("Parser SLR1")
    text, automaton, parser = Execute_SLR1(G)
    print(text)
    print()

    print("Parser LR1")
    text, automaton, parser = Execute_LR1(G)
    print(text)
    print()

    print("Parser LALR")
    text, automaton, parser = Execute_LALR(G)
    print(text)
    print()

