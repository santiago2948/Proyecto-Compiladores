from grammar.grammar import *
from LL1.ll1_parsing import *
import random

def nuevoNoterminal(dicc):
    letras=["Z", "X", "E", "W", "Q", "P", "M", "Y"]
    control=True
    while control:
        no_terminal= random.choice(letras)
        if no_terminal not in dicc: control=False
    return no_terminal

def leftRecursion(producciones):
    modificado=producciones.copy()
    for nonTerminal in producciones:
        new_rules=["e"]
        temporal=[]
        #creacion de un nuevo no terminal no presente en la gramatica para reemplazar las producciones con LR
        nuevo=nuevoNoterminal(modificado)
        for i in range(0,len(producciones[nonTerminal])):
            regla=producciones[nonTerminal][i]
            #coomparacion de las producciones para verificar si tienen recursion izquierda
            if regla[0]==nonTerminal: new_rules.append(regla[1:]+nuevo)
            #si hubo una produccion co recursion entonces a las reglas sin recursion se les concatena el nuevo no terminal
            elif len(new_rules)>1:temporal.append(regla+nuevo)
        #agregacion de las nuevas reglas
        if len(new_rules)>1:
            modificado[nuevo]=new_rules
            modificado[nonTerminal]=temporal
        pass

    return modificado

def ingresarGramatica(index):
    #aca se ingresan los simbolos no terminales
    N= input().split()
    #aca se pide el ingreso de reglas de produccion
    P={}
    lr_controlller=False
    for _ in range(int(index[1])):
        rule=input().split('-')
        if rule[0] not in P:
            P[rule[0]]=[rule[1]]
        else:
            regla=rule[1]
            #se da preoridad a las recursiones izquierdas
            if regla[0]==rule[0]: 
                lr_controlller=True
                P[rule[0]].insert(0,rule[1])
            else:  P[rule[0]].append(rule[1])
        pass
    if lr_controlller:
        P=leftRecursion(P)
    analisis= Grammar(N,P)
    print(analisis.grammar_configuration())
    return analisis



if __name__=="__main__":
     #aca se ingresan los 4 indices separados por espacio: numero de no terminales, numero de reglas y cadenas a revisar
    index= input().split()
    gramatica = ingresarGramatica(index)
    ll1parsing= LL1Parsing(gramatica)
    ll1parsing.createTable()
