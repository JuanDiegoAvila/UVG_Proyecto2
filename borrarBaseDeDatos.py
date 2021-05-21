from neo4j import GraphDatabase as GD

baseDeDatos = GD.driver(uri="bolt://localhost:7687", auth=("neo4j", "jamon123"))
sesion = baseDeDatos.session()  # se establece la coneccion con la base de datos.

def comando(ses, cm):  # recibe la sesion y el comando a ejecutar
    return ses.run(cm)


sesion.run("MATCH (n:Artista)-[r:Canta]->() DELETE r")
sesion.run("MATCH (n:Cancion)-[r:Pertenece_a]->() DELETE r")
sesion.run("MATCH (n:Cancion)-[r:Genera]->() DELETE r")
sesion.run("MATCH (n:Artista)-[r:Crea]->() DELETE r")
sesion.run("MATCH (n) DELETE n")