def backtrakin(lista, n, base, count=0, soluciones=[]):
    if n<count:
        return
    elif count==n:
        soluciones.append(base[:])
    for i in lista:
        count+=i
        base.append(i)
        backtrakin(lista, n, base, count, soluciones)
        count-=i
        base.pop()
    return soluciones

#print(backtrakin([2,4,6,8], 10, []))

def diag(array, index) -> bool:
    for i in range(index):
        if abs(array[index] - array[i]) == abs(index - i):
            return False
    return True

def isBack(array, index):
    for i in range(index):
        if array[index] == array[i]:
            return False
    return True

def reinas(array, index=0):
    if index == len(array):
        respuesta.append(array[:])  # Guardar una copia de la solución válida
        return

    for i in range(len(array)):
        array[index] = i
        if isBack(array, index) and diag(array, index):
            reinas(array, index + 1)

respuesta = []
"""
reinas([None] * 4)  
print(respuesta)
"""

def contador(lista,i):
    contador=0
    for i in lista:
        contador+=i
    return contador

def combinaciones(array, n, solucion=[]):
    counter=contador(solucion,0)
    if counter==n and solucion not in soluciones:
        soluciones.append(solucion[:])

    for i in array:
        solucion.append(i)
        if counter<=n:
            combinaciones(array,n,solucion)
        if len(solucion)>0:
            solucion.pop()
    pass
soluciones=[]
combinaciones([2, 3, 6, 7],7)
print(soluciones)