class Grammar:
    def __init__(self, N, P):
        self.alphabet = []
        self.N = N
        self.P = P
        self.first={}
        self.follow={}
        self.faux=[]
        self.beta = ""
        self.reglas = []
        self.follows_priority = {}

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

    def firstRule(self, rule):
        firstr=[]
        for i in rule:
            if i in self.P:
                firstr.extend(self.first[i])
                if "e" in firstr: firstr.remove("e")
                if "e" not in self.first[i]: return firstr
            else:
                firstr.append(i)
                return firstr
        firstr.append("e")
        return firstr

    def isLL1(self):
        for n in self.P:
            for i in range(0,len(self.P[n])):
                f_rule_alpha = self.firstRule(self.P[n][i])
                for j in range(i+1, len(self.P[n])):
                    f_rule_beta= self.firstRule(self.P[n][j])
                    intersection= set(f_rule_alpha) & set(f_rule_beta)
                    #aplying the first filter of ll(1) grammars where if the intersection between beta first and alpha first is diferent to empty this grammar is not ll(1)
                    if len(intersection)>0:
                        return False
                    #aplying secondary copnditions to first intersect with follow of A if "e" in first of one of both rules
                    if "e" in f_rule_beta:
                        intersection= set(f_rule_beta) & set(self.follow[n])
                        if len(intersection)>0:
                            return False
                        pass
                    if "e" in f_rule_alpha:
                        intersection= set(f_rule_alpha) & set(self.follow[n])
                        if len(intersection)>0:
                            return False
        return True

#____________________________________________________________________________

    #Follow requeriments:

    # It needs to classify wich type of rule is each one in the  grammar.
    # We could to create a stack for each type of rule.
    # There are 2 types of rules:

    # 1: Rules as follows: A->aBβ where First(β) != e
    # do: First(β)-{e} into Follow(B)
    #Insertion of new elements.
    #  
    # 2: Rules as follows: A->aB or A->aBβ where First(β) = e
    #do: Follow(A) into Follow(B)
    # Agregation of existant elements. 
    #
    

    def Follow(self, Non_T)->None:

        if Non_T == self.N[0]:
            self.follow[Non_T] = ['$']

        if Non_T not in self.follow:
            self.follow[Non_T] = []
     
        #Traverse the Non_T's rule
        for char in self.P[Non_T]:
            for B in char:
                #Follows
                if B in self.N:
                    if B not in self.follow:
                        self.follow[B] = []                 
                    if(self.is_type_1(char, B)):
                        #agregation of new elements
                        #b is β
                        #print("Beta: " + self.beta)
                        for b in self.beta:
                            if b in self.N:
                                #First(β)-{e} into Follow(B)
                                if b not in self.follow[B]:
                                    if 'e' not in self.first[b]:
                                        for k in self.first[b]:
                                            if k not in self.follow[B]:
                                                self.follow[B].append(k)
                                                #print(f" First(beta)  {self.follow}") 
                                                break   
                                        break
                            if b not in self.follow[B]:
                                self.follow[B].append(b)
                                #print(f"Character: {self.follow}")
                                break 

                    #Rule is type 2 A->aB or A->aBβ where First(β) = e        
                    else:
                         #ordenation
                         #Non_T is A 
                        #print("Type_2")    
        
                        self.follows_priority[Non_T] = B
                        '''for l in self.follow[Non_T]:
                            if l not in self.follow[B]:
        
                                self.follow[B].append(l)'''
                        
        #Insert and organize each follow
        #Follow(A) into Follow(B)
        pass                        
#________________________________________________________________________________                        
                                              
    def is_type_1(self, rule, B):
        alpha = ""
        beta = ""
        B_index = 0
        if len(rule) > 1:
            for i in range(0, len(rule)):
                if(rule[i] == B):
                    B_index = i

            #set alpha if is not e
            if (B_index > 0):
                for j in range(0, B_index):
                    alpha += rule[j]

            if (B_index == 0):
                alpha = 'e'
            #set beta if is not e
            if B_index < len(rule) - 1:
    
                for k in range(B_index + 1, len(rule)):
                    beta += rule[k]

            if (B_index == len(rule) -1 and beta == ''):
                beta = 'e'        

            #print(f'Alpha: {alpha} B: {B} beta: {beta}')    

            #Validate if is type 1
            for char in beta:
                if char in self.N:
                    if 'e' in self.first[char]:
                        print("e is in First(beta)")
                        return False
                    else:
                        print("rule is type 1")
                        self.beta = beta
                        
                        return True
                if char == 'e':
                    print('rule is not type 1')
                    return False                   
            #print("rule is type 1")  
            self.beta = beta   
            return True   

        else:
            #print("is not type 1")
            return False
        
#________________________________________________________________        
        
    def apply_follow(self):
        for i in self.N:
            self.Follow(i)   

        #To manage the type 2 rules  A->aB or A->aBβ where First(β) = e   
        #print(f'Priority: {self.follows_priority}')
        for A in self.N:
            if A in self.follows_priority:
             
             #Follow(A) into Follow(B)   
             for B in self.follows_priority[A]:
                for char_A in self.follow[A]: 
                    #print(f'follow de {A}: {self.follow[A]}')
                    if char_A not in self.follow[B] and char_A != '':   
                        self.follow[B].append(char_A)    
        print(self.follow)
        pass
 
    def grammar_configuration(self):
        self.First()
        self.apply_follow()
        return self.isLL1()
        