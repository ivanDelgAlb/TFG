from pymongo import MongoClient
import csv

dataFrame_T1 = [
    ['ds', 'y', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error']
]

dataFrame_T2 = [
    ['ds', 'y', 'T1', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error']
]

dataFrame_Prob0 = [
    ['ds', 'y', 'T2', 'T1', 'probMeas1Prep0', 'readout_error']
]

dataFrame_Prob1 = [
    ['ds', 'y', 'T2', 'probMeas0Prep1', 'T1', 'readout_error']
]

dataFrame_error = [
    ['ds', 'y', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'T1']
]

def dataFrame(nombre_maquina):
    
    mongo_uri = "mongodb+srv://ivandelgadoalba:claveMongo@cluster0.pn3zcyq.mongodb.net/"
    client = MongoClient(mongo_uri)

    collection_name_Origen = "derivado"

    db = client["TFG"]

    datos = db[collection_name_Origen].find({"name": nombre_maquina})

    for item in datos:
        dataFrame_T1.append([item['date'], item['properties']['qubits'][0]['media'], item['properties']['qubits'][1]['media'], item['properties']['qubits'][2]['media'], item['properties']['qubits'][3]['media'], item['properties']['qubits'][4]['media']])
        dataFrame_T2.append([item['date'], item['properties']['qubits'][1]['media'], item['properties']['qubits'][0]['media'], item['properties']['qubits'][2]['media'], item['properties']['qubits'][3]['media'], item['properties']['qubits'][4]['media']])
        dataFrame_Prob0.append([item['date'], item['properties']['qubits'][2]['media'], item['properties']['qubits'][0]['media'], item['properties']['qubits'][1]['media'], item['properties']['qubits'][3]['media'], item['properties']['qubits'][4]['media']])
        dataFrame_Prob1.append([item['date'], item['properties']['qubits'][3]['media'],  item['properties']['qubits'][0]['media'], item['properties']['qubits'][1]['media'], item['properties']['qubits'][2]['media'], item['properties']['qubits'][4]['media']])
        dataFrame_error.append([item['date'], item['properties']['qubits'][4]['media'],  item['properties']['qubits'][0]['media'], item['properties']['qubits'][1]['media'], item['properties']['qubits'][2]['media'], item['properties']['qubits'][3]['media']])

    nombre_archivo = 'dataframeT1.csv'

    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        
        escritor_csv = csv.writer(archivo_csv)
        
        for fila in dataFrame_T1:
            escritor_csv.writerow(fila)

    nombre_archivo = 'dataframeT2.csv'

    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        
        escritor_csv = csv.writer(archivo_csv)
        
        for fila in dataFrame_T2:
            escritor_csv.writerow(fila)

    nombre_archivo = 'dataframeProb0.csv'

    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        
        escritor_csv = csv.writer(archivo_csv)
        
        for fila in dataFrame_Prob0:
            escritor_csv.writerow(fila)

    nombre_archivo = 'dataframeProb1.csv'

    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        
        escritor_csv = csv.writer(archivo_csv)
        
        for fila in dataFrame_Prob1:
            escritor_csv.writerow(fila)
        
    nombre_archivo = 'dataframeError.csv'

    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        
        escritor_csv = csv.writer(archivo_csv)
        
        for fila in dataFrame_error:
            escritor_csv.writerow(fila)

    print("Extracción finalizada")


dataFrame("ibm_brisbane");
