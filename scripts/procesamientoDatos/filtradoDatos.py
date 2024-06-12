from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri_origen = os.getenv("MONGO_URI_MARINA_PART1")
mongo_uri_destino = os.getenv("MONGO_URI_IVAN_PART1")
client_origen = MongoClient(mongo_uri_origen)
client_destino = MongoClient(mongo_uri_destino)

collection_name_Destino = "derivado"
collection_name_Origen = "data"

db_origen = client_origen["TFG"]
db_destino = client_destino["TFG"]

db_destino[collection_name_Destino].drop()
print("Colección borrada con éxito")

datos = db_origen[collection_name_Origen].find()
for dato in datos:

    qubits = dato['properties']['qubits']

    qubits_sin_atributos = []

    for qubit in qubits:
        qubits_sin_atributo = []
        for q in qubit:
            if q['name'] != 'frequency' and q['name'] != 'anharmonicity':
                qubits_sin_atributo.append(q)
        qubits_sin_atributos.append(qubits_sin_atributo)

    dato['properties']['qubits'] = qubits_sin_atributos
    
    dato['properties'].pop('general', None)
    dato['properties'].pop('general_qlists', None)
    dato.pop('configuration', None)
    
    collection = db_destino[collection_name_Destino]
    collection.insert_one(dato)

print("Se han seleccionado los datos correctamente")


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
