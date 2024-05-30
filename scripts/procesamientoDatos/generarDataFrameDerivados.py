from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de MongoDB Atlas (reemplaza con tus propios valores)
mongo_uri = os.getenv("MONGO_URI_MARINA_PART1")
client = MongoClient(mongo_uri)

# Nombre de la colección en MongoDB Compass
collection_name_Destino = "dataFrame"
collection_name_Origen = "derivado"

# Conectarse a la base de datos en MongoDB Atlas
db = client["TFG"]

# Borro la colección por si tenía algún dato
db[collection_name_Destino].drop()
print("Colección borrada con éxito")

datos = db[collection_name_Origen].find()


for documento in datos:
    nombre_maquina = documento['name']
    # Verificar si el nombre de la máquina ya existe en la base de datos
    documento_existente = db[collection_name_Destino].find_one({"name": nombre_maquina})
    if documento_existente:
        # Si el documento ya existe, actualiza los datos
        # Supongamos que tus nuevos datos están en un diccionario llamado 'nuevos_datos'
        nuevos_datos = {
            "date": documento['date'],
            "T1": documento['properties']['qubits'][0],
            "T2": documento['properties']['qubits'][1],
            "prob_meas0_prep1": documento['properties']['qubits'][2],
            "prob_meas1_prep0": documento['properties']['qubits'][3],
            "readout_error": documento['properties']['qubits'][4]
        }

        db[collection_name_Destino].update_one({"_id": documento_existente["_id"]},{"$push": {"data": nuevos_datos}})
        print(f"Datos actualizados para {nombre_maquina}")
    else:
        datos = {
            "name": nombre_maquina,
            "data": [{
                "date": documento['date'],
                "T1": documento['properties']['qubits'][0],
                "T2": documento['properties']['qubits'][1],
                "prob_meas0_prep1": documento['properties']['qubits'][2],
                "prob_meas1_prep0": documento['properties']['qubits'][3],
                "readout_error": documento['properties']['qubits'][4]
            }]
        }
        db[collection_name_Destino].insert_one(datos)
        print(f"Nuevo documento creado para {nombre_maquina}")

print("Iteración sobre la base de datos completada")