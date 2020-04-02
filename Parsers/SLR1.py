from Parsers.Utils.FirstFollow import *
from Parsers.Utils.ShiftReduceParser import *
from Parsers.Utils.ShiftReduceUtils import *
from cmp.pycompiler import Grammar
from cmp.pycompiler import Item

class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        self.G = self.G.AugmentedGrammar(True)
        firsts = compute_firsts(self.G)
        follows = compute_follows(self.G, firsts)
        automaton = build_LR0_automaton(self.G).to_deterministic()

        for i, node in enumerate(automaton):
            node.idx = i

        prodOk = self.G.startSymbol.productions[0]
        posOk = len(prodOk.Right)

        conflicts = []
        
        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                
                if item.IsReduceItem:
                    if item.production == prodOk and posOk == item.pos:
                        self._register(self.action, (idx, self.G.EOF.Name),(self.OK, 1), conflicts, node)
                        continue
                    
                    for follow in follows[item.production.Left]:
                        self._register(self.action, (idx, follow.Name), (self.REDUCE, item.production), conflicts, node)
                        
                else:
                    if item.NextSymbol.IsTerminal:
                        self._register(self.action, (idx, item.NextSymbol.Name), (self.SHIFT, node.transitions[item.NextSymbol.Name][0].idx), conflicts, node)
                    else:
                        self._register(self.goto, (idx, item.NextSymbol.Name), (node.transitions[item.NextSymbol.Name][0].idx), conflicts, node)
        
        return automaton, conflicts

    @staticmethod
    def _register(table, key, value, conflicts, node):
        if key in table and not value in table[key]:
            if (key[1], node) not in conflicts:
                conflicts.append((key[1], node))
            if not value in table[key]:
                table[key].append(value)
        else:
            table[key] = [value]

    