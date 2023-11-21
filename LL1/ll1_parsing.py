
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

    def analize(self, string)->bool:
        self.createTable()
        #Get the String to Analize       
        stack_input = [i for i in string]
        stack_input.append('$') 
        stack_states = [self.grammar.N[0]]
        stack_states.append('$')  
        while len(stack_input) >= 1 and len(stack_states) >= 1:
            #Save the current top in each stack
            top_1 = stack_input[0]
            top_2 = stack_states[0]
            #Using the parse table to replace the current state, to the rule that we need to generate the input 
            if top_1 =='$' and top_2 == '$': 

                return True
            
            elif top_2 == top_1:
                stack_input.pop(0)
                stack_states.pop(0) 
            
                
            elif top_2 in self.grammar.N and top_1 in self.table[top_2]:

                table_rule = [i for i in self.table[top_2][top_1]]  
                stack_states.pop(0)
                table_rule_r=table_rule[::-1]
                for i in table_rule_r:
                    if i!="e":
                        stack_states.insert(0, i)

            else:
                return False
                                       