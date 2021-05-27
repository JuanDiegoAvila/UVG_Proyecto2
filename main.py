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


def buscar(ingresado,opcion,ses):

    existe = True
    if opcion == "nombre":
        actual = ses.run("MATCH (a:Artista{nombre:'%s'}) RETURN a"%ingresado)
        lista = [nodo["a"] for nodo in actual]
        if(len(lista)==0):
            existe = False

    elif opcion == "cancion":
        actual = ses.run("MATCH (c:Cancion{nombre:'%s'}) RETURN c"%ingresado)
        lista = [nodo["c"] for nodo in actual]
        if(len(lista)==0):
            existe = False

    elif opcion == "animo":
        actual = ses.run("MATCH (c:Animo{nombre:'%s'}) RETURN c"%ingresado)
        lista = [nodo["c"] for nodo in actual]
        if(len(lista)==0):
            existe = False

    elif opcion == "genero":
        actual = ses.run("MATCH (c:Genero{nombre:'%s'}) RETURN c"%ingresado)
        lista = [nodo["c"] for nodo in actual]
        if(len(lista)==0):
            existe = False

    return existe

def agregar(ses):

    nombre = input("\nIngrese el nombre del artista que creo la cancion -> ")
    cancion = input("Ingrese el nombre de la cancion -> ")
    genero = input("Ingrese el genero de la cancion -> ")
    animo = input("Describa en una palabra como se siente al escuchar la cancion -> ")
    # se define quien canta la cancion.

    artista_existe = buscar(nombre.lower(),"nombre",ses)
    genero_existe = buscar(genero.lower(),"genero",ses)
    cancion_existe = buscar(cancion.lower(),"cancion",ses)
    animo_existe = buscar(animo.lower(),"animo",ses)

    nombre = nombre.lower()
    cancion = cancion.lower()
    genero = genero.lower()
    animo = animo.lower()

    if cancion_existe == True:
        print("\n La cancion que ha ingresado ya existe ! ")
    else:
        if artista_existe == True and genero_existe == True and animo_existe == True:

            comando_canciones = "CREATE (c:Cancion {nombre: '%s'}) RETURN c" %cancion
            comando(ses, comando_canciones)

            comando_canta = "MATCH (a:Artista {nombre:'%s'}),(b:Cancion{nombre:'%s'}) MERGE (a)-[r:Canta]->(b)" % (nombre,cancion)
            comando(ses, comando_canta)

            # se define el genero de la cancion.
            comando_g = "MATCH (a:Cancion {nombre:'%s'}),(b:Genero{nombre:'%s'}) MERGE (a)-[r:Pertenece_a]->(b)" % (cancion,genero)
            comando(ses, comando_g)

            comando_an = "MATCH (a:Cancion {nombre:'%s'}),(b:Animo{nombre:'%s'}) MERGE (a)-[r:Genera]->(b)" % (cancion,animo)
            comando(ses, comando_an)

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

        
def comando(ses, cm):
    # recibe la sesion y el comando a ejecutar
    return ses.run(cm)