
from pymongo import MongoClient
import csv

mongo_uri = "mongodb+srv://ivandelgadoalba:claveMongo@cluster0.pn3zcyq.mongodb.net/"
client = MongoClient(mongo_uri)

collection_name_Origen = "derivado"

db = client["TFG"]

dataFrame = [
    ['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error']
]

def normalized(nombre_maquina):
    formatearNombre = nombre_maquina.split("_")[1].capitalize()

    datos = db[collection_name_Origen].find({"name": nombre_maquina})

    for item in datos:

        fila = []

        T1 = item['properties']['qubits'][0]['mediana']
        T2 = item['properties']['qubits'][1]['mediana']
        probMeas0Prep1 = item['properties']['qubits'][2]['mediana']
        probMeas1Prep0 = item['properties']['qubits'][3]['mediana']
        readout_error = item['properties']['qubits'][4]['mediana']
        
        fila_min = min(T1,T2, probMeas0Prep1, probMeas1Prep0, readout_error)
        fila_max = max(T1,T2, probMeas0Prep1, probMeas1Prep0, readout_error)

        T1_norm = (T1 - fila_min) / (fila_max - fila_min)
        T2_norm = (T2 - fila_min) / (fila_max - fila_min)
        probMeas0Prep1_norm = (probMeas0Prep1 - fila_min) / (fila_max - fila_min)
        probMeas1Prep0_norm = (probMeas1Prep0 - fila_min) / (fila_max - fila_min)
        readout_error_norm = (readout_error - fila_min) / (fila_max - fila_min)

        fila.extend([T1_norm, T2_norm, probMeas0Prep1_norm, probMeas1Prep0_norm, readout_error_norm])

        dataFrame.append(fila)

    nombre_archivo = 'dataframe_'+ formatearNombre + '.csv'

    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerows(dataFrame)

    print("El archivo {} ha sido creado exitosamente.".format(nombre_archivo))

normalized("ibm_brisbane")
