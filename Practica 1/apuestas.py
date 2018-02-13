import random
import math
'''Simulated annealing para el problema de las apuestas, en este caso resolveremos el problema para 5 apuestas triples.

-Se recomienda, para fijar ideas, comenzar con un sistema de 5 triples, espacio que consta de 3^5=243 apuestas.
-Considerar un código de recubrimiento óptimo a distancia R=1 de dicho espacio, que consta de 27 apuestas (resultante de orlar con los tres resultados posibles de un quinto partido las 9 apuestas de la reducción de 4 triples que facilita el código Hamming ternario adecuado).
-Determinar un sistema condicionado para esos 5 partidos a triple (por ejemplo, 2 variantes, con 1-2 equis y 1-2 doses; que supone un espacio de 80 apuestas).
-Ver cuántas de esas 27 apuestas recubren el nuevo espacio condicionado.
-Programar una rutina de enfriamiento del acero y ver la cantidad de puntos que devuelve el mejor recubrimiento que sea capaz de encontrar, comparando el resultado con el anterior. (Hasta aquí, sobre 0,6 puntos).
-Reproducir todo el esquema en otro sistema múltiple de entre los propuestos en las diapositivas. (Esto puntúa sobre 0,4).

Variantes: 2
Equis: 1,2
Doses: 1,2

Total: 80 apuestas

'''

#Generamos las 27 apuestas que parten de las 9 apuestas de la reducción de 4 triples que facilita el código Hamming ternario
#Una apuesta se representara con una lista del tamaño de numero de partidos para los que se esta apostando para el caso de 5 apuestas una apuesta podría ser: [1,0,2,1,1]
# El número posible de valores para una apuesta es 0, 1, 2

#Partiendo de la reduccionde 4 triples


def genera_codigo_recubrimiento_5():
    cuatro_triples = [[0,0,0,0],[1,1,1,0],[2,2,2,0],[2,1,0,1],[0,2,1,1],[1,0,2,0],[1,2,0,2],[2,0,1,2],[0,1,2,2]]

    #Montamos ahora las apuestas para 5 triples a partir de cuatro triples

    cinco_triples = []
    
    resultados = [0,1,2]
    apuesta_actual = []
    for apuesta in cuatro_triples:
        for resultado in resultados:
            apuesta_actual = apuesta[:]
            apuesta_actual.append(resultado)
            cinco_triples.append(apuesta_actual[:])
            apuesta_actual.pop()
               
    return cinco_triples
   

def genera_todas_apuestas(tamanyo):
    '''Metodo usado para generar las apuestas de '''
    apuestas = []
    numero_apuestas_totales = (3 ** tamanyo)
    
    for i in range(numero_apuestas_totales):
        apuesta_lst = []
        apuesta_str = cambio_base(i,3,tamanyo)
        
        for c in apuesta_str:
            apuesta_lst.append(c)
            
        apuestas.append(apuesta_lst)
    return apuestas

def cambio_base(decimal, base, tamanyo_apuesta):
    '''Metodo auxiliar usado para cambiar un número de base decimal a la base indicada fijando el número de bits de salida'''
    conversion = ''
    while decimal // base != 0:
        conversion = str(decimal % base) + conversion
        decimal = decimal // base
        
    
    resultado = str(decimal) + conversion
    numero_ceros = tamanyo_apuesta -  len(resultado)
    
    cadena_ceros = ''
    
    for i in range(numero_ceros):
        cadena_ceros = cadena_ceros + '0'
    
   
    return cadena_ceros + resultado

def cambia_bit_aleatorio(apuesta,R):
    '''Cambia R numero de bits aleatorios de una apuesta'''
    apuesta_alterada = apuesta[:]
    bits_restantes_por_cambiar = list(range(0,len(apuesta_alterada)))
    

    contador_bits_cambiados = 1
    
    while contador_bits_cambiados <= R:
        posibilidades = ['0','1','2']
        if contador_bits_cambiados == 1:
            aleatorio1 = random.randint(0, len(bits_restantes_por_cambiar) - 1)
            
            posicion_editar = bits_restantes_por_cambiar[aleatorio1]
            
            valor_apuesta_anterior = apuesta_alterada[posicion_editar]
            posibilidades.remove(valor_apuesta_anterior)
            
            aleatorio2 = random.randint(0, len(posibilidades) - 1)
            apuesta_alterada[posicion_editar] = posibilidades[aleatorio2]
            
            #Borramos la posicion elegida para que no se modifique mas
            bits_restantes_por_cambiar.pop(posicion_editar)
            
            
        else:
            #Generamos un numero aleatorio entre 0 y 1, si es menor que 0.5 no cambiamos y si es
            # superior a 0.5 cambiamos
            aleatorio3 = random.random()
            if aleatorio3 >= 0.5:
                aleatorio1 = random.randint(0, len(bits_restantes_por_cambiar) - 1)
                
                posicion_editar = bits_restantes_por_cambiar[aleatorio1]
                valor_apuesta_anterior = apuesta_alterada[posicion_editar]
                posibilidades.remove(valor_apuesta_anterior)
                
                aleatorio2 = random.randint(0, len(posibilidades) - 1)
                apuesta_alterada[posicion_editar] = posibilidades[aleatorio2]
                
                #Borramos la posicion elegida para que no se modifique mas
                bits_restantes_por_cambiar.pop(posicion_editar)
            
        
        contador_bits_cambiados = contador_bits_cambiados + 1
        
    
    return apuesta_alterada
    

def filtra_apuestas(lista_todas_apuestas, lista_num_variantes, lista_num_equis, lista_num_doses):
    '''Del total de apuestas solo nos devuelve aquellas que pasen el filtro de las variantes
    Parametros:
    lista_todas_apuestas: Lista que contiene todas las apuestas de un determinado tamaño
    lista_num_variantes: lista que contiene las posibles variantes a generar
    lista_num_equis: lista del numero de equis de las variantes
    lista_num_doses: lista del numero de doses de las variantes
    '''
    
    filtro = [] # Lista de posibles cantidades de 1 y 2 
    apuestas_filtradas = []
    #Generamos las combinaciones posibles
    for variante in lista_num_variantes:
        for equis in lista_num_equis:
            
            num_doses = variante - equis
            if num_doses in lista_num_doses:
                filtro.append([equis,num_doses])
        
        for doses in lista_num_doses:
            num_equis = variante - doses
            if num_equis in lista_num_equis:
                #Si ya estaba generada en el filtro no la añadas de nuevo
                if [num_equis,doses] not in filtro:
                    filtro.append([num_equis,doses])
    
    #Filtramos las apuestas
    for apuesta in lista_todas_apuestas:
        #print("-----------")
        #print("apuesta: " + str(apuesta))
        num_equis_apuesta = 0
        num_doses_apuesta = 0
        #Contamos el numero de X y 2 que tiene la apuesta
        for elem in apuesta:
            #print("elem: " + str(elem))
            if elem == '1':
                num_equis_apuesta = num_equis_apuesta + 1
            if elem == '2':
                num_doses_apuesta = num_doses_apuesta + 1
            
        # Nos quedamos con aquellas apuestas que pasen el filtro
        #print("num equis : " + str(num_equis_apuesta))
        #print("num doses : " + str(num_doses_apuesta))
        if [num_equis_apuesta,num_doses_apuesta] in filtro:
            apuestas_filtradas.append(apuesta)
    #print(filtro)    
    return apuestas_filtradas
        
def elige_n_apuestas_aleatorias(lista_apuestas, num_apuestas):
    '''Elige un numero n aleatorio de apuestas de entre la lista de apuestas'''
    todas_apuestas = lista_apuestas[:]
    apuestas_aleatorias = []
    
    contador = 1
    while contador <= num_apuestas:
        num_aleatorio = random.randint(0, len(todas_apuestas) - 1)
        apuesta = todas_apuestas[num_aleatorio]
        #Insertamos la apuesta seleccionada en las apuestas aleatorias
        apuestas_aleatorias.append(apuesta)
        #Borramos de la lista de apuestas totales la apuesta que acabamos de seleccionar
        todas_apuestas.pop(num_aleatorio)
        contador = contador + 1
        
    return apuestas_aleatorias


def calcula_puntos_cubiertos_por_C_de_S(C,S,R,tamanyo_apuesta):
    '''Devuelve los puntos recubiertos por C en S, con un radio dado'''
    puntos_cubiertos = []
    
    for apuesta_s in S:
        for apuesta_c in C:
            distancia = 0
            contador = 0
            while contador < tamanyo_apuesta:
                valor_apuesta_s = apuesta_s[contador]
                valor_apuesta_c = apuesta_c[contador]
                
                if valor_apuesta_s != valor_apuesta_c:
                    distancia = distancia + 1
                
                contador = contador + 1
                
            if distancia <= R:
                puntos_cubiertos.append(apuesta_s)
    
    return puntos_cubiertos

def puntos_sin_cubrir_por_C_de_S(puntos_totales,puntos_cubiertos):
    '''Obtener los puntos que estan sin cubrir'''
    puntos_sin_cubrir = puntos_totales[:]
    
    for elem in puntos_cubiertos:
        if elem in puntos_sin_cubrir:
            puntos_sin_cubrir.remove(elem)
        
    
    return puntos_sin_cubrir

#Simulated annealing
    
def simulated_annealing_apuestas(n,T,frio,veces,R,tamanyo_apuesta,S):
    #n = 5 # El número de bolas de radio R con que se pretende recubrir el espacio S
    
    C = [] # Conjunto de n apuestas concretas de los partidos en el sistema
    N = [] # Puntos del espacio (apuestas) S sin cubrir por la unión de las bolas de C
    #T = 2 # Temperatura inicial (por ejemplo, 2; se puede probar con distintos valores)
    #frio = 0.95
    #veces = 5
    #R = 1 # Radio de apuestas que se pretende cubrir
    
    #Generamos S
    # S contiene todas las apuestas sin ningun filtro
    
    
    C = [] #Al principio en C hay que coger un numero n aleatorio de apuestas de S
    N = S[:]
    
    
    C = elige_n_apuestas_aleatorias(S, n)
    print("Apuestas aleatorias elegidas: "+ str(C) + " - Numero de apuestas: " + str(len(C)))
    
    #En N tenemos en cada momento el numero de puntos sin cubrir
    
    print("-------------------------------------------------------")
    while len(N) > 0:
        #print("Longitud N: " + str(len(N)))
        
        for elem in C:
            j = 1
            anterior = elem[:]
            #print("Valor de T: " + str(T)) 
            while j <= veces:
                
                print("--------------------------------------")
                #print("Vez: " + str(j))
                #Creamos una variable temporal
                C_aux = C[:]
                N_aux = N[:]
                d = cambia_bit_aleatorio(elem,R)
                #print("elem: " + str(elem) + " - elem alterado: " + str(d))
                # Actualizamos C_aux
                #print("c_aux: " + str(C_aux) + " - elem para borrar: " + str(anterior))
                C_aux.remove(anterior)
                C_aux.append(d)
                
                puntos_cubiertos_despues_cambio = calcula_puntos_cubiertos_por_C_de_S(C_aux,S,R,tamanyo_apuesta)
                
                N_aux = puntos_sin_cubrir_por_C_de_S(S,puntos_cubiertos_despues_cambio)
                # Preguntamos si nos mejora el numero de apuestas que recubre
                print("Longitud N antes: " + str(len(N)) + " - Longitud N ahora: " + str(len(N_aux)))
                if len(N_aux) <= len(N):
                    #print("Actualizo porque es mejor")
                    #Actualizar C y N
                    anterior = d[:]
                    C = C_aux[:]
                    N = N_aux[:]
                else:
                    num_aleatorio = random.random()
                    probabilidad = math.exp(-(1*len(N))/(T*1.0))
                    #print("Probabilidad: " + str(probabilidad) + " - num aleatorio: " + str(num_aleatorio))
                    if probabilidad < num_aleatorio:
                        #print("Permito actualizar con probabilidad")
                        #Actualizar C y N
                        anterior = d[:]
                        C = C_aux[:]
                        N = N_aux[:]
               
                j = j + 1 
                          
        T = T * frio
    
    print("Apuestas recubridoras: "+ str(C))
    
  
#Generamos las apuestas de un tamaño
S1 = genera_todas_apuestas(5)
#print("Apuestas totales: "+ str(S1) + " - Numero de apuestas: " + str(len(S1)))
# Filtramos las apuestas generadas indicando: lista de apuestas a filtrar, variantes, equis, doses
S1 = filtra_apuestas(S1,[2],[1,2],[1,2])
print("Apuestas filtradas: "+ str(S1) + " - Numero de apuestas: " + str(len(S1)))

#resultado1 = simulated_annealing_apuestas(12,2,0.95,2,1,4,S1)

