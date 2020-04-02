from Parsers.LR1 import *
from cmp.automata import State, multiline_formatter
from cmp.pycompiler import Grammar
from cmp.pycompiler import Item
from cmp.utils import ContainerSet
from Parsers.Utils.FirstFollow import *
from Parsers.Utils.ShiftReduceParser import *
from Parsers.Utils.ShiftReduceUtils import *

class LALRParser(LR1Parser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        
        automaton = self.build_LR1_automaton(G)
        automaton = self.Compact_Automata(automaton)

        prodOk = G.startSymbol.productions[0]
        posOk = len(prodOk.Right)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        conflicts = []

        for node in automaton:
            idx = node.idx
            for item in node.state:
                if item.IsReduceItem:
                    if item.production == prodOk and posOk == item.pos and G.EOF in item.lookaheads:
                        self._register(self.action, (idx, G.EOF.Name),(self.OK, 1), conflicts, node)
                        continue
                    
                    for lookahead in item.lookaheads:
                        self._register(self.action, (idx, lookahead.Name), (self.REDUCE, item.production), conflicts, node)
                        
                else:
                    if item.NextSymbol.IsTerminal:
                        self._register(self.action, (idx, item.NextSymbol.Name), (self.SHIFT, node.transitions[item.NextSymbol.Name][0].idx), conflicts, node)
                    else:
                        self._register(self.goto, (idx, item.NextSymbol.Name), (node.transitions[item.NextSymbol.Name][0].idx), conflicts, node)
        
        return automaton, conflicts