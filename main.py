import crearBaseDeDatos as CBD
import borrarBaseDeDatos as BBD

por_genero = {}
por_artista = {}
por_animo = {}


def porArtista(ses):
    canciones = ses.run("MATCH (a:Artista) return a")
    lista = [nodo["a"] for nodo in canciones]
    for n in lista:
        print(n["nombre"])
    return canciones


def porGenero(ses):
    canciones = ses.run("MATCH (A:Genero) return A")
    return canciones


def porAnimo(ses):
    canciones = ses.run("MATCH (A:Animo) return A")
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
