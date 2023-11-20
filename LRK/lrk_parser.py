
class LRK:
    def __init__(self, grammar):
        self.grammar=grammar
        self.P=grammar.P
        self.first= grammar.first
        self.follow= grammar.follow
        self.P= grammar.P
        self.extension=grammar.start+"'"
        self.S=grammar.start
        self.kernels=[]
        self.P[self.extension]=[self.S]
        pass
    
    def clousure_start(self, item, clousure=[]):
        control=item["N"]
        rule=item["item"][0]
        point=item["item"][1]
        
        if rule[point] in self.P:
            for regla in self.P[rule[point]]:
                add= {"N": rule[point], "item": [regla, 0]}
                if add not in clousure:
                    clousure.append(add)
                if regla[0] in self.P and regla[0]!=control:
                    clousure= self.clousure_start(add, clousure)
                pass
        return clousure

    def addKernel(self, item):
        if item not in self.kernels:
            self.kernels.append(item)
        return self.kernels.index(item)
        
    def clousure(self, items):
        agregados=[]

        pass

    def createAutomata(self):
        automata={} 
        item_inicial= {"N": self.extension,"item": [self.P[self.extension], 0]}
        item=self.addKernel(item_inicial)
        clousure=self.clousure_start(item_inicial, [item_inicial])
        automata[item]={"clousure": clousure}
        print(self.kernels)
        print(automata)
        pass

