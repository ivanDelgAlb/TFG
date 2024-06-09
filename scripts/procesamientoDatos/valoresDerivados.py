from pymongo import MongoClient
import statistics

import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri_Origen = "mongodb+srv://marinasayago2002:clavetfg@tfg-part3.jphrtkl.mongodb.net/"
#mongo_uri_Origen = os.getenv("MONGO_URI_MARINA_PART2")
client_Origen = MongoClient(mongo_uri_Origen)

#mongo_uri_Destino = os.getenv("MONGO_URI_IVAN_PART2")
mongo_uri_Destino = "mongodb+srv://ivandelgadoalba:claveMongo@cluster0.pn3zcyq.mongodb.net/"
client_Destino = MongoClient(mongo_uri_Destino)

collection_name_Destino = "derivado"
collection_name_Origen = "data"

db_Origen = client_Origen["TFG"]
db_Destino = client_Destino["TFG"]


def calcMedia(datos, nqubit, atributo):
    media = 0
    cont = 0

    for dato in datos:
        if nqubit > 0:
            if len(dato['qubits']) == nqubit:
                for gate in dato['parameters']:
                    if gate['name'] == 'gate_error':
                        media += gate['value']
                        cont += 1
        else:
            for qubit in dato:
                if qubit['name'] == atributo:
                    media += qubit['value']
                    cont += 1

    if cont > 0:
        media = media / cont
    
    return media


def calcMediana(datos, nqubit, atributo):
    valores = []

    for dato in datos:
        if nqubit > 0:
            if len(dato['qubits']) == nqubit:
                for gate in dato['parameters']:
                    if gate['name'] == atributo:
                        valores.append(gate['value'])
        else:
            for qubit in dato:
                if qubit['name'] == atributo:
                    valores.append(qubit['value'])
    valores.sort()
    n = len(valores)
    
    if n % 2 == 0:
        mediana = (valores[n//2 - 1] + valores[n//2]) / 2
    else:
        mediana = valores[n//2]

    return mediana


def calcDesviacion(datos, nqubit, atributo):
    valores = []

    for dato in datos:
        if nqubit > 0:
            if len(dato['qubits']) == nqubit:
                for gate in dato['parameters']:
                    if gate["name"] == atributo:
                        valores.append(gate['value'])
        else:
            for qubit in dato:
                if qubit["name"] == atributo:
                    valores.append(qubit['value'])

    if len(valores) < 2:
        return None

    desviacion_estandar = statistics.stdev(valores)
    return desviacion_estandar

    
datos = db_Origen[collection_name_Origen].find()

for dato in datos:

    qubits = dato['properties']['qubits']
    qubits_derivados = []

    gates = dato["properties"]["gates"]
    gates_derivados = []
        
    atributos = ["T1", "T2", "prob_meas0_prep1", "prob_meas1_prep0", "readout_error", "gate_error", "gate_length"]
    nqubits = [1, 2]

    for atributo in atributos:

        if atributo != "gate_error" and atributo != "gate_length":

            documento = {
                "name": atributo,
                "media": calcMedia(qubits, -1, atributo),
                "mediana": calcMediana(qubits, -1, atributo),
                "desviacion": calcDesviacion(qubits, -1, atributo)
            }

            qubits_derivados.append(documento)
        
        else:

            for nqubit in nqubits:
                documento = {
                    "name": atributo,
                    "nºqubits": nqubit,
                    "media": calcMedia(gates, nqubit, atributo),
                    "mediana": calcMediana(gates, nqubit, atributo),
                    "desviacion": calcDesviacion(gates, nqubit, atributo)
                }
                gates_derivados.append(documento)


    dato['properties']['qubits'] = qubits_derivados
    dato['properties']['gates'] = gates_derivados

    dato['properties'].pop('general', None)
    dato['properties'].pop('general_qlists', None)
    dato.pop('configuration', None)


    collection = db_Destino[collection_name_Destino]

    collection.insert_one(dato)
    print(f"Datos insertados con éxito para el archivo: {dato['date']}, máquina: {dato['name']}")
    

print("Se han insertado todos los valores derivados correctamente")
