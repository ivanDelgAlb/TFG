from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de MongoDB Atlas (reemplaza con tus propios valores)
mongo_uri_origen = os.getenv("MONGO_URI_MARINA_PART1")
mongo_uri_destino = os.getenv("MONGO_URI_IVAN_PART1")
client_origen = MongoClient(mongo_uri_origen)
client_destino = MongoClient(mongo_uri_destino)

# Nombre de la colección en MongoDB Compass
collection_name_Destino = "derivado"
collection_name_Origen = "data"

# Conectarse a la base de datos en MongoDB Atlas
db_origen = client_origen["TFG"]
db_destino = client_destino["TFG"]

# Borro la colección por si tenía algún dato
db_destino[collection_name_Destino].drop()
("Colección borrada con éxito")

datos = db_origen[collection_name_Origen].find()
#numero_elementos = len(datos)
#(numero_elementos)
for dato in datos:
    # Eliminar atributos no deseados
    qubits = dato['properties']['qubits']

    qubits_sin_atributos = []

    for qubit in qubits:
        qubits_sin_atributo = []  # Inicializa una lista vacía para cada qubit
        for q in qubit:
            if q['name'] != 'frequency' and q['name'] != 'anharmonicity':
                qubits_sin_atributo.append(q)  # Agrega el qubit a la lista si cumple con las condiciones
        qubits_sin_atributos.append(qubits_sin_atributo)


    # Crear una nueva lista de qubits sin los que tienen nombre 'frequency'

    
    # Asignar la lista de qubits sin 'frequency' de vuelta a la propiedad 'qubits' del dato
    dato['properties']['qubits'] = qubits_sin_atributos
    
    
    # Eliminar otros atributos no deseados
    dato['properties'].pop('general', None)
    dato['properties'].pop('general_qlists', None)
    dato.pop('configuration', None)
    
    # Insertar documento modificado en la colección de destino
    collection = db_destino[collection_name_Destino]
    collection.insert_one(dato)

("Se han seleccionado los datos correctamente")


'''
    gates = dato['properties']['gates']

    gates_sin_atributos = []
    for gate in gates:
        gates_sin_atributo = [] 
        for g in gate['parameters']:
            if g['name'] == 'gate_error' or g['name'] == 'gate_length':
                gates_sin_atributo.append(g)  # Agrega el qubit a la lista si cumple con las condiciones
        gates_sin_atributos.append(gates_sin_atributo)
        dato['properties']['gates'] = gates_sin_atributos
'''  
