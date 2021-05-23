from neo4j import GraphDatabase as GD
import pandas as pd

baseDeDatos = GD.driver(uri="bolt://localhost:7687", auth=("neo4j", "jamon123"))
sesion = baseDeDatos.session()  # se establece la coneccion con la base de datos.


def crear():
    # de primero se debe leer el csv para tener toda la informacion y se va agregando a la base de datos

    informacion = pd.read_csv('DatosIniciales.csv', ';')
    existe = sesion.run("MATCH (n) RETURN count(n)")

    if existe.single()[0] == 0:
        artistas = pd.DataFrame(informacion['Artistas']).values.tolist()
        generos = pd.DataFrame(informacion['Generos']).values.tolist()
        estados_de_animo = pd.DataFrame(informacion['Estados de Animos']).values.tolist()
        canciones = pd.DataFrame(informacion['Canciones']).values.tolist()

        # agrega los generos en la base de datos.
        temp = []
        for i in generos:
            if (temp.count(i) < 1):
                comando_generos = "CREATE (a:Genero {nombre: '" + i[0].lower() + "'}) RETURN a"
                comando(sesion, comando_generos)

            temp.append(i)

        # agrega los artistas en la base de datos
        temp.clear()
        for i in artistas:
            if (temp.count(i) < 1):
                comando_artista = "CREATE (a:Artista {nombre: '%s'}) RETURN a" % i[0].lower()
                comando(sesion, comando_artista)

            temp.append(i)

        # agrega los estados de animo en la base de datos
        temp.clear()
        for i in estados_de_animo:
            if (temp.count(i) < 1):
                comando_animo = "CREATE (a:Animo {nombre: '%s'}) RETURN a" % i[0].lower()
                comando(sesion, comando_animo)

            temp.append(i)

        for i in canciones:
            comando_canciones = "CREATE (c:Cancion {nombre: '%s'}) RETURN c" % i[0].lower()
            comando(sesion, comando_canciones)

        # luego de crear los datos se crean las relaciones entre los nodos.

        inf_temporal = pd.DataFrame(informacion).values.tolist()
        for t in inf_temporal:  # lista que contiene lista con toda la informacion de cada cancion.
            # se define quien canta la cancion.

            comando_canta = "MATCH (a:Artista {nombre:'%s'}),(b:Cancion{nombre:'%s'}) MERGE (a)-[r:Canta]->(b)" % (
            t[0].lower(), t[3].lower())
            comando(sesion, comando_canta)

            # se define el genero de la cancion.
            comando_g = "MATCH (a:Cancion {nombre:'%s'}),(b:Genero{nombre:'%s'}) MERGE (a)-[r:Pertenece_a]->(b)" % (
            t[3].lower(), t[1].lower())
            comando(sesion, comando_g)

            comando_an = "MATCH (a:Cancion {nombre:'%s'}),(b:Animo{nombre:'%s'}) MERGE (a)-[r:Genera]->(b)" % (
            t[3].lower(), t[2].lower())
            comando(sesion, comando_an)

            comando_crea = "MATCH (a:Artista {nombre:'%s'}),(b:Genero{nombre:'%s'}) MERGE (a)-[r:Crea]->(b)" % (
            t[0].lower(), t[1].lower())
            comando(sesion, comando_crea)

    return baseDeDatos


def comando(ses, cm):
    # recibe la sesion y el comando a ejecutar
    return ses.run(cm)
