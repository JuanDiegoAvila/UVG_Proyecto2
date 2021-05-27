import crearBaseDeDatos as CBD
import borrarBaseDeDatos as BBD

por_genero = {}
por_artista = {}
por_animo = {}


def porArtista(ses):

    #Se ingresa el artista que desea buscar las canciones
    artista = input("\nIngrese el nombre del artista que quiere escuchar -> ")
    #Se busca el mach de que canciones canta el artista para guardarlas
    canciones = ses.run("MATCH (a:Artista{nombre:'%s'})-[:Canta]->(c:Cancion) return c"% artista.lower())

    #Se agregan a una lista
    lista = [nodo["c"] for nodo in canciones]
    
    #Se van imprimiento las canciones encontradas que hicieron mach con el artista ingresado
    if len(lista) == 0:
        print("\nEl artista que ha ingresado no existe.")
    else:
        print("\nLas canciones que te recomendamos de "+artista+" son:")
        for i in range(0,len(lista)):
            print("\t-> "+lista[i]["nombre"])

    return canciones


def porGenero(ses):
    #Se ingresa el genero por el que se desea buscar
    genero = input("\ningrese el genero que desea escuchar -> ")
    
    #Se buscan las canciones que son generadas por el genero (valgame la redundancia)
    canciones = ses.run("MATCH (c:Cancion)-[:Pertenece_a]->(a:Genero{nombre:'%s'}) return c"% genero.lower())
    
    #Se agregan a una lista
    lista = [nodo["c"] for nodo in canciones]
    lista2 = []

    #Se busca el artista de cada una de las canciones
    for n in lista:
        temp = n["nombre"]
        artista = ses.run("MATCH (a:Artista)-[:Canta]->(c:Cancion{nombre:'%s'}) return a"% temp)
        t = [nodo["a"] for nodo in artista]
        for n in t:
            lista2.append(n["nombre"])
    
    #Se imprime la lista de canciones con el artista
    if len(lista) == 0:
        print("\nEl genero que ha ingresado no existe.")
    else:
        print("\nLas canciones que te recomendamos de "+genero+" son:")
        for i in range(0,len(lista)):
            print("\t-> "+lista[i]["nombre"]+" de "+lista2[i])
            
    return canciones


def porAnimo(ses):
    #Se ingresa el animo por el que quiere escuchar las canciones
    animo = input("\ningrese el estado de animo que desea escuchar -> ")
    
    #Se busca las canciones que generan ese estado de animo
    canciones = ses.run("MATCH (c:Cancion)-[:Genera]->(a:Animo{nombre:'%s'}) return c,a"% animo.lower())
    
    lista = [nodo["c"] for nodo in canciones]
    lista2 = []
    
    #Se busca el artista de las canciones
    for n in lista:
        temp = n["nombre"]
        artista = ses.run("MATCH (a:Artista)-[:Canta]->(c:Cancion{nombre:'%s'}) return a"% temp)
        t = [nodo["a"] for nodo in artista]
        for n in t:
            lista2.append(n["nombre"])
    
    #Se muestran en pántalla las canciones y los artistas
    if len(lista) == 0:
        print("\nEl estado de animo que ha ingresado no existe.")
    else:
        print("\nLas canciones que te recomendamos de "+animo+" son:")
        for i in range(0,len(lista)):
            print("\t-> "+lista[i]["nombre"]+" de "+lista2[i])
    return canciones


def agregar(ses):
    cancion = ""
    return cancion


def eliminar(ses):
    cancion = ""
    return cancion


baseDeDatos = CBD.crear()  # crea la base de datos al iniciar el programa.
sesion = baseDeDatos.session()
# BBD.borrar()

print("\nBienvenido al sistema de recomendaciones de musica ! \n")
print("Para comenzar selecciona una de las siguientes opciones para poder recomendarte una cancion:")
print("\t[ 1 ] Buscar por artista")
print("\t[ 2 ] Buscar por Genero")
print("\t[ 3 ] Buscar por Estado de Animo")
print("\t[ 4 ] Agregar una nueva cancion")
print("\t[ 5 ] Eliminar una cancion")
print("\t[ 6 ] Salir")

while (True):
    opcion = input(" \nOpcion -> ")

    try:
        opcion = int(opcion)
        if opcion == 1:
            porArtista(sesion)
        elif opcion == 2:
            porGenero(sesion)
        elif opcion == 3:
            porAnimo(sesion)
        elif opcion == 4:
            agregar(sesion)
        elif opcion == 5:
            eliminar(sesion)
        elif opcion == 6:
            print("\n Gracias por utilizar el sistema de recomendaciones SpotyZeer ! ")
            break
        else:
            print("\nIngrese un numero valido entre 1 y 6")

    except:
        print("\nIngrese valores numericos!")
