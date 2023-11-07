class Grammar:
    def __init__(self, N, P):
        self.alphabet = []
        self.N = N
        self.P = P
        self.first={}
        self.Follow={}
        self.reglas = []
        for i in self.P:
            self.reglas.extend(self.P[i])

    def FirsRec(self, N):
        for i in self.P[N]:
            if i[0] not in self.N:
                if N in self.first: self.first[N].append(i[0]) 
                else: self.first[N]=[i[0]]
            elif i in self.N:
                self.FirstRec(i)
            pass
        pass

    def First(self):
        for n in self.N: self.FirsRec(n)
        pass
        print(self.first)


if __name__=="__main__":
    #aca se ingresan los 4 indices separados por espacio: numero de no terminales, numero de reglas y cadenas a revisar
    index= input().split()
    #aca se ingresan los simbolos no terminales
    N= input().split()
    #aca se pide el ingreso de reglas de produccion
    P={}
    for _ in range(int(index[1])):
        rule=input().split('-')
        if rule[0] not in P:
            P[rule[0]]=[rule[1]]
        else:
            P[rule[0]].append(rule[1])
        pass
    analisis= Grammar(N,P)
    #strings son las cadenas a analizar
    analisis.First()