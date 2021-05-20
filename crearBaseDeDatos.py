from neo4j import GraphDatabase as GD

baseDeDatos = GD.driver(uri="bolt://localhost:####", auth=("SpotyZeer", "jamon123"))
sesion = baseDeDatos.session()  # se establece la coneccion con la base de datos.


def comando(ses, cm): # recibe la sesion y el comando a ejecutar
    return ses.run(cm)

#de primero se debe leer el csv para tener toda la informacion y se va agregando a la base de datos