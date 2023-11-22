from grammar.grammar import *

def ingresarGramatica(index):
    #aca se ingresan los simbolos no terminales
    N= input().split()
    S=N[0]
    #aca se pide el ingreso de reglas de produccion
    P={}
    for _ in range(int(index[1])):
        rule=input().split('-')
        if rule[0] not in P:
            P[rule[0]]=[rule[1]]
        else:
            regla=rule[1]
            #se da preoridad a las recursiones izquierdas
            if regla[0]==rule[0]: 
                P[rule[0]].insert(0,rule[1])
            else:  P[rule[0]].append(rule[1])
        pass
    analisis= Grammar(N,P,S)
    return analisis



if __name__=="__main__":
    gramaticas={}
    #veces a ejecutar
    times_to_excecute = int(input())
    for i in range(0, times_to_excecute):
        #aca se ingresan los 3 indices separados por espacio: numero de no terminales, numero de reglas y cadenas a revisar
        index= input().split()
        gramatica = ingresarGramatica(index)
        
        strings=[]
        for _ in range(0, int(index[2])):
            string=input()
            strings.append(string)
            pass
        gramaticas[gramatica]=strings
        
    for grammar in gramaticas:
        for string in gramaticas[grammar]:
            
            grammar.Parser(string)