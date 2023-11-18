
class LL1Parsing:
    def __init__(self, grammar) -> None:
        self.first= grammar.first
        self.follow= grammar.follow
        self.P= grammar.P
        self.table={}
        pass

    def firstRule(self, rule):
        firstr=[]
        for i in rule:
            if i in self.P:
                firstr.extend(self.first[i])
                if "e" in firstr: 
                    firstr.remove("e")
                if "e" not in self.first[i]: 
                    return firstr
            else:
                firstr.append(i)
                return firstr
        firstr.append("e")
        return firstr
    
    def createTable(self):
        for n in self.P:
            rulesparser={}
            for rule in self.P[n]:
                first= self.firstRule(rule)
                for i in first:
                    if i=="e":
                        for k in self.follow[n]:
                            rulesparser[k]=rule
                            pass
                    else:
                        rulesparser[i]=rule
                pass
            self.table[n] = rulesparser
        print(self.table)