class Grammar:
    def __init__(self, N, P):
        self.alphabet = []
        self.N = N
        self.P = P
        self.respuesta = False
        self.index = 0
        self.reglas = []
        for i in self.P:
            self.reglas.extend(self.P[i])


    def ParserRec(self,string, generada):
        if len(generada)>len(string):
            return
        if [i for i in string]==generada:
            self.respuesta=True
            return
        
        for i in range(len(generada)):
            if generada[i] in self.N:
                for k in self.P[generada[i]]:
                    nueva=generada.copy()
                    nueva.pop(i)
                    if len(k)>0:
                        for j in range(0,len(k)):
                            nueva.insert(i+j, k[j])
                    else:
                        generada.insert(i, k)
                    self.ParserRec(string, nueva)

    def Parser(self, string):
        self.respuesta=False
        for i in self.reglas:
            self.ParserRec(string, [k for k in i])
        return self.respuesta


if __name__=="__main__":
    #aca se ingresan los 4 indices separados por espacio: numero de no terminales, numero de reglas y cadenas a revisar
    index= input().split()
    #aca se ingresan los simbolos no terminales
    N= input().split()
    #aca se pide el ingreso de reglas de produccion
    P={}
    strings=[]
    for _ in range(int(index[1])):
        rule=input().split('-')
        if rule[0] not in P:
            P[rule[0]]=[rule[1]]
        else:
            P[rule[0]].append(rule[1])
        pass
    analisis= Grammar(N,P)
    
    for _ in range(int(index[-1])):
        strings.append(input())
        pass

    for i in strings:
        print(analisis.Parser(i))
    
    pass