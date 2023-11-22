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
        self.automata={} 
        self.P[self.extension]=[self.S+"$"]
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
    
    def calculate_clousure(self, rules, visitados=[]):

        #item: {'N': "S", 'item': ['S', 0], 'actions': []}, letter: S lista: [{'N': "S'", 'item': ['S', 1], 'actions': []}]

        #
        for item in rules:
            
            #accedemos al no terminal correspondinete a la regla del item
            #accedemos a la regla que representa este item
            rule = item["item"][0] # 'item': 'S'
            #accedemos a el id de donde se encuentra el punto de este item
            point = item["item"][1] # 'items':'0'

            #este condicional modera que cuando el indice esté en un no terminal se agreguen todas sus reglas a el clousure
            #en caso tal de que el indice que indica la posicion del punto del item en cuestion sea igual a su len osea se encuentre en la posicion final se retorna []
            if len(rule) == point:
                continue
                
            elif rule[point] in self.P:
                #se agregan las reglas una por una
                for regla in self.P[rule[point]]:
                    #se da la estructura de item para que se pueda dar de manera estandarizada
                    add= {"N": rule[point], "item": [regla, 0]}
                    #se verifica que el item en cuestion no haya sido agregado previamente
                    if add not in rules:
                        rules.append(add)
                    #se verifica que el no terminal que se envia a la recursion no sea el mismo que se envio en un inicio para evitar recursiones infinitas
                    if regla[0] in self.P  and regla[0] not in visitados:
                        visitados.append(regla[0])
                        rules= self.calculate_clousure(rules, visitados)
                pass

        return rules


    def addKernel(self, item):
        """""""""extension,
        la funcion addkernel cumple la funcion de crear los kernels si estos no fueron creados previamente o si fueron creados retorna sus ids para asi
        no tener tablas repetidas y poder hacer la conexion en forma de grafo de forma estandarizada por asi decirlo, se trata de una especie de base de datos donde almacenamos nuestros 
        kernels y sus ids para acceder a estos
        """#se itera sobre cada uno de los items en la lista que se recibe como argumento en la cual se deben de encontrar los items involucrados en la transicion de una tabla a otra
        
        if item not in self.kernels:
            self.kernels.append(item)
        return self.kernels.index(item)
        
    def conexions(self, items):
        """""""""
        la funcion conexiones nos retorna los simbolos con los cuales se va a hacer un avance en una tabla para avanzar a otra tabla es decir si hay transiciones con las letras a, b o c nos las retornara
        para asi poder hacer el automata de forma organizada creando las nuevas tablas y sus conexiones facilmente solo iterando sobre los items y tomando aquellos con los cuales se avanzaria con un simbolo determinado
        """
        conexiones=[]
        #iteramos sobre los items y miramos donde esta apuntando el indice que representa el punto, hecho esto agregamos este simbolo en caso de que se pueda hacer transición en la tabla con el si este ya se encuentra en la
        #lista de conexiones lo omitimos
        for i in range(0, len(items)):
            index=items[i]["item"][1]
            
            if index<len(items[i]["item"][0]):
                letter=items[i]["item"][0][index]
                if letter not in conexiones and letter !="e":
                    conexiones.append(letter)
        return conexiones
        

    def initialItems(self):
        #la funcion initialItems crea el primer conjunto de items del automata l base a el cual se crearan posteriormente sus ramificaciones
        item_inicial= {"N": self.extension,"item": [self.P[self.extension][0], 0]}
        item=self.addKernel(item_inicial)
        clousure=self.calculate_clousure( [item_inicial])
        #se agrega este conjunto de items al automata 
        self.automata[item]={"clousure": clousure}
        
    def createTable(self, ide, letra, rules):
        #create table creara las otras tablas y las agregara al automata, para esto se le envia las reglas de la transición con una letra especifica para calcularle a esto el clousure y crearle su kernel correspondiente
        clousure=self.calculate_clousure(rules)
        kernel = rules[0]
        _id=self.addKernel(kernel)
        obj={"clousure":clousure}
        #actons es el aributo de el diccionario el cul contienen las transiciones
        if "actions" not in self.automata[ide]:
            self.automata[ide]["actions"]={letra:_id}
        else:
            if letra not in self.automata[ide]["actions"]:
                self.automata[ide]["actions"][letra]=_id
            else:
                return False

        if _id not in self.automata:
            self.automata[_id]=obj
            #se envia el clousure para crear las tablas de las hojas como una busqueda en frofundidd
            self.createAutomata_rec(clousure, _id)

    def createAutomata_rec(self, items, _id):
        #obtenemos las conexiones que se pueden realizar con nuestro conjunto de items para iterar sobre estos y hacer las transiciones de manera organizada
        conex=self.conexions(items)
        #se realiza la anteriormente mensionada iteracion
        for letter in conex:
            aux=[] #el auxiliar se usa para guardar todas las reglas cuyo indice de transición sea el mismo
            for item in items:
                #obtenemos el indice de transicion de la regla sobre la cual estamos iterando para poder saber donde estaria el punto
                index=item["item"][1]
                #se compara la letra de esta iteracion con la letra en el indice de nuestra regla para saber si son iguales y en caso tal
                #agregamos a la lista de la transición de esta letra para esto usamos el indice que indica donde estaria el punto
                if index < len(item["item"][0]):    
                    if item["item"][0][index] == letter:
                        rule=item.copy()
                        aux.append({"N":rule["N"], "item":[rule["item"][0], rule["item"][1]+1]})
            answer=self.createTable(_id, letter,aux)
            if answer==False:
                return False
            
                
    def createReduccions(self):
        #la funcion create reduccion crea las reduccionesde la tabla en los accions agregando todas las reglas en las cuales el indicados del punto se encuentre en el el final de la regla
        #es decir que seai giaual al len de la regla
        for _id in self.automata:
            for item in self.automata[_id]["clousure"]:
                    #se verifica qeu el indicador del punto se encuentre a el final de la cadena o si la regla deriva direcamente en epsilon
                    if item["item"][1] == len(item["item"][0]) or item["item"][0]=="e":
                        #la extension de la cadena no se agrega en la tabla para realizar reducciones
                        if item["N"] != self.extension:
                            regla=item["item"].copy()
                            regla+= item["N"]
                            #se usa el follow del no terminal para añadir las reducciones que se realizan en los terminales contenidos en este
                            for letter in self.follow[item["N"]]: 
                                if "actions" not in self.automata[_id]:
                                    self.automata[_id]["actions"]={letter: regla}
                                else:
                                    #se verifica que no haya conflico a la hora de agregar las reglas, es decir que ya no haya una regla o moviminto en el
                                    #terminal o no terminal que se vaya a agregar, en caso de ser asi se retorna falso ya que la gramatica no es LL(1)
                                    if letter not in self.automata[_id]["actions"]:
                                        self.automata[_id]["actions"][letter]= regla
                                    else:
                                        return False

    def createAutomata(self):
        self.initialItems()
        
        if self.createAutomata_rec(self.automata[0]["clousure"], 0)==False:
            return False
        
        if self.createReduccions()==False:
            return False
        tabla={}
        for _id in self.automata:
                if "actions" in self.automata[_id]:
                    if self.automata[_id]["clousure"][0]["N"] == self.extension and len(self.automata[_id]["clousure"][0]["item"][0]) -1 ==self.automata[_id]["clousure"][0]["item"][1]:
                        tabla[_id] = self.automata[_id]["actions"]
                        tabla[_id]["$"] = "aceptar"
                        pass
                    else: 
                        tabla[_id] = self.automata[_id]["actions"]
        return tabla

    
    def analize_lrk(self, string)->bool:
        table = self.createAutomata()
        
        if table == False:
            return 'error'
    
        stack_states = []
        stack_states.append(0)
        stack_states.append('$')
        stack_input =[i for i in string]
        stack_input.append('$')
        stack_symbols = []

        #print("Configurations")
        #< symbols analyzed , states , pila de String>
        # []    [0$]     [aacbb$]
        #Caso base: cuando el simbolo inicial esté en el stack del string
         
         # un estado shift = numero verificar si lo que devuelve es int
        while( len(stack_input) >= 1 ):
            
            top_3 = stack_input[0]
            
            top_2 = stack_states[0]
            if len(stack_symbols) > 1:
                top_1 = stack_symbols[0]
                
                
            #print(f'< {stack_symbols} | {stack_states} | {stack_input} >')    
            
            if top_3 not in table[top_2]:
                return False
            
            elif table[top_2][top_3] == "aceptar":
                #Base Case when the simbol and the state shifts into accept
                return True
            elif type(table[top_2][top_3]) == int:
                #Shift state
                if top_3 not in table[top_2]:
                    return False
                stack_states.insert(0, table[top_2][top_3])
                stack_symbols.append(top_3)
                stack_input.pop(0)
            
                
            elif type(table[top_2][top_3]) == list:
                #reduction state
                if top_3 not in table[top_2]:
                    return False
                rule_len = table[top_2][top_3][1]
                if rule_len > len(stack_states):
                    return False
                else:
                    for _ in range(rule_len):
                        stack_states.pop(0)
                        stack_symbols.pop(-1)

                    stack_symbols.append(table[top_2][top_3][2]) 
                    top_2=stack_states[0]
                    goto = table[top_2][stack_symbols[-1]] 
                    stack_states.insert(0, goto)
            else:

                return False        
                       
