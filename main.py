class Grammar:
    def __init__(self, N, P):
        self.alphabet = []
        self.N = N
        self.P = P
        self.first={}
        self.Follow={}
        self.faux=[]

    def FirstRec(self, N):
        #Set of rules of the non terminal N
        for i in self.P[N]:
            #Base case
            #Is a terminal?
            if i[0] not in self.N:
                #N is in First?
                self.agregation_function(N, i[0])
                for x in self.faux:
                    self.agregation_function(x, i[0])
            elif i[0] in self.N:
                for k in range(0, len(i)):
                    if i[k] in self.N:
                            self.faux.append(N)
                            self.FirstRec(i[k])   
                            if "e" not in self.P[i[k]]:
                                break
                    else: self.agregation_function(N, i[k])

        if len(self.faux)>0:
            self.faux.pop(-1)

    def agregation_function(self,N, T):
        if N in self.first:
            #To fill the dictionary without repeated terminals 
            if T not in self.first[N]: 
                self.first[N].append(T)     
        else: 
            self.first[N]=[T]
            
    def First(self):
        for n in self.N: 
            self.FirstRec(n)
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