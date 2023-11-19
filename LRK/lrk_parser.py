
class LRK:
    def __init__(self, grammar):
        self.grammar=grammar
        self.P=grammar.P
        self.first= grammar.first
        self.follow= grammar.follow
        self.P= grammar.P
        self.extension=grammar.start+"'"
        self.S=grammar.start
        self.P[self.extension]=[self.S]
        pass
    
    def clousure(self, kernel,N,items=[]):
        item=kernel[N][0]
        index=kernel[N][1]

        pass

    def parsing(self):
        items_iniciales={} 
        items_iniciales[self.extension]=self.P[self.extension].append(0)
        self.clousure(items_iniciales)

        pass

if [1, {"h":["hola", 0]}] ==[1, {"h":["hola", 0]}]:
    print("hello")