from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText
from cmp.pycompiler import *
from LL1Test import *
from SLR1ParserTest import *
from LR1Test import *
from LALRTest import *
from GrammarOperations import *
import pydot

def JumpWhiteSpaces(text, index):
    while index < len(text) and (text[index] == ' ' or text[index] == '\n'):
            index += 1
            
    if index == len(text):
        return None
    
    return index        

def ConsumeToWhiteSpace(text, index):
    result = ""
    while index < len(text) and text[index] != ' ' and text[index] != '\n' and text[index] != ';' and text[index] != '|' and text[index] != '-' and text[index] != '>':
        result += text[index]
        index += 1
    
    if len(result) == 0:
        if text[index] == '|':
            result = '|'
            index += 1
            
        elif text[index] == ';':
            result = ';'
            index += 1
            
        else:    
            return None, index
    
    return result, index

def ConsumeArrow(text, index):
    index = JumpWhiteSpaces(text, index)
    if index is None:
        return len(text), False
    
    if index + 2 >= len(text):
        return index, False
     
    if text[index] != '-' or text[index + 1] != '-' or text[index + 2] != '>':
        return index, False
    
    index += 3
    
    return index ,True    

def FormProduction(text, index, G, symbols, G2, symbols2):
    
    right = [[]]
    right2 = [[]]
    i = 0
    while True:
       
        index = JumpWhiteSpaces(text, index)
        if index is None:
            return None, len(text), None
        
        string, index = ConsumeToWhiteSpace(text, index)
        
        
        if string is None:
            return None, index, None
        
        if string == ";":
            if len(right[i]) == 0:
                return None, index, None
            
            return right, index, right2
        
        if string == '|':
            i += 1
            right.append([])
            right2.append([])
            continue
        
        try:
            right[i].append(symbols[string])
            right2[i].append(symbols2[string])
            
        except KeyError:
            if string[0] >= 'A' and string[0] <= 'Z':
                s = G.NonTerminal(string)
                right[i].append(s)
                symbols[string] = s
                s2 = G2.NonTerminal(string)
                right2[i].append(s2)
                symbols2[string] = s2
            else:
                s = G.Terminal(string)
                right[i].append(s)
                symbols[string] = s
                s2 = G2.Terminal(string)
                right2[i].append(s2)
                symbols2[string] = s2
      
def GetGrammar(text, symbols, symbols2):
    
    if len(text) == 1:
        lbl.insert('1.0',"Escribe la gramatica")
        return None, None
    
    start = True
    
    index = 0
    G = Grammar()
    G2 = Grammar()
    
    symbols['e'] = G.Epsilon
    symbols['\n'] = G.EOF
    symbols2['e'] = G2.Epsilon
    symbols2['\n'] = G2.EOF
    while index < len(text):
        #ignorar espacios en blanco
        index = JumpWhiteSpaces(text, index)
        if index is None:
            return G, G2
        
        if text[index] < 'A' or text[index] > 'Z':
            lbl.insert('1.0',"Se esperaba un no Terminal " + text[index])
            return None, None
        
        current, index = ConsumeToWhiteSpace(text, index)
        
        if current is None:
            return G, G2
        
        if start:
            left = symbols[current] = G.NonTerminal(current, True)
            start = False
            left2 = symbols2[current] = G2.NonTerminal(current, True)
            
            
        else:
            try:
                left = symbols[current]
                left2 = symbols2[current]
            except KeyError:
                left = symbols[current] = G.NonTerminal(current)
                left2 = symbols2[current] = G2.NonTerminal(current)
        
        
        index, Ok = ConsumeArrow(text, index)
        if not Ok:
            lbl.insert('1.0', "Se esperaba --> " + text[index - 1])
            return None, None
           
        right, index, right2 = FormProduction(text, index, G, symbols, G2, symbols2) 
        
        if right is None:
            lbl.insert('1.0', "Se esperaba una produccion " + text[index - 1])
            return None, None
    
        for productions in right:
            sentence = productions[0]
            for i in range(1, len(productions)):
                sentence = sentence + productions[i] + G.Epsilon
            
            left %= sentence

        for productions in right2:
            sentence2 = productions[0]
            for i in range(1, len(productions)):
                sentence2 = sentence2 + productions[i] + G2.Epsilon
        
            left2 %= sentence2
        
        index += 1
    return G, G2
        
def ToTerminals(cadena, symbols):
    string = []
    for char in cadena:
        string.append(symbols[char])
        
    return string    

def clicked():
    symbols = {}
    symbols2 = {}
    grammar_type = combo.get()
    lbl.delete("1.0", END)
    window2 = Tk()
    window2.title("Parsea la cadena")
    window2.geometry('400x200')
    
    entry = Entry(window2)
    entry.grid(column = 0, row = 1)
    l = Label(window2)
    l.grid(column = 0, row = 2)
    G, G2 = GetGrammar(st.get("1.0", END), symbols, symbols2)
    
    def parsea():
        cadena = entry.get()
        string = ToTerminals(cadena, symbols)
        string.append(G.EOF)
        if grammar_type == 'll1':
            derivation_tree = Derivation_Tree(parser, string)
            
        else:
            derivation_tree = Derivation_Tree_ShiftReduce(parser, string)

        derivation_tree.graph().write_png("Derivation_Tree.png")
       
    btn2 = Button(window2, text = "Click", command = parsea)
    btn2.grid(column = 1, row = 0)

    if not G is None:
        text = ""
        
        if grammar_type == 'll1':
            text1, automata_regular = Execute(G)
            text += text1
            text1, parser = Execute_LL1(G)
            text += text1

        elif grammar_type == 'slr':
            text1, automata, parser = Execute_SLR1(G)
            automata.graph().write_png("Automata1.png")
            text += text1

        elif grammar_type == 'lr1':
            text1, automata, parser = Execute_LR1(G)
            automata.graph().write_png("Automata1.png")
            text += text1

        elif grammar_type == 'lalr':
            text1, automata, parser = Execute_LALR(G)
            automata.graph().write_png("Automata1.png")
            text += text1
            
        
        if not grammar_type == 'll1':
            text1, automata_regular = Execute(G2)
            text += text1

        if not automata_regular is None:
            automata_regular.graph().write_png("Regular_Automata.png")
            
        lbl.insert('1.0', text)
        
       

window = Tk()
window.title("Gestor de Gramatica")
window.geometry('600x500')

combo = Combobox(window)
combo['values'] = ('ll1', 'slr','lr0', 'lr1', 'lalr', 'regular')
combo.current(0)
combo.grid(column = 0, row = 0)

btn = Button(window, text = "Click", command = clicked)
btn.grid(column = 1, row = 0)

st = ScrolledText(window, width = 35, height = 30)
st.grid(column = 0, row = 1)


lbl = ScrolledText(window, width = 111, height = 30)
lbl.grid(column = 1, row = 1)


window.mainloop()

