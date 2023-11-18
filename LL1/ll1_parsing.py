
class LL1Parsing:
    def __init__(self, grammar) -> None:
        self.grammar=grammar
        self.first= grammar.first
        self.follow= grammar.follow
        self.P= grammar.P
        self.table={}
        pass
    
    def createTable(self):
        for n in self.P:
            rulesparser={}
            for rule in self.P[n]:
                first= self.grammar.firstRule(rule)
                for i in first:
                    if i=="e":
                        for k in self.follow[n]:
                            rulesparser[k]=rule
                            pass
                    else:
                        rulesparser[i]=rule
                pass
            self.table[n] = rulesparser
        self.table

    def analize(self):
        self.createTable()
        pass