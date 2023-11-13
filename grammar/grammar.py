class Grammar:
    def __init__(self, N, P):
        self.alphabet = []
        self.N = N
        self.P = P
        self.first={}
        self.Follow={}
        self.faux=[]
        self.reglas = []

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
    
    def follow(self):
        for n_t in self.P:
            for regla in self.P[n_t]:
                for c in range(0,len(regla)-1):
                    if regla[c] in self.N:
                        if regla[c+1] in self.N:
                            #entonces el first de regla[c+1] esta en follow de regla[c]

                            pass          

    def follow_agregation(self,N, T):
        if N in self.Follow:
            #To fill the dictionary without repeated terminals 
            if T not in self.first[N]: 
                self.first[N].append(T)     
        else: 
            self.first[N]=[T]             
           