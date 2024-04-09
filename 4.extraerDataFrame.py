from pymongo import MongoClient
import csv

mongo_uri = 'mongodb+srv://Marina:mongoTFG@tfg.qet3gme.mongodb.net/'
client = MongoClient(mongo_uri)

collection_name_Origen = 'dataFrame'

db = client['TFG']

datos = db[collection_name_Origen].find({'name': 'ibm_brisbane'})

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

for item in datos[0]['data']:
    dataFrame_T1.append([item['date'], item['T1']['media'], item['T2']['media'], item['prob_meas0_prep1']['media'], item['prob_meas1_prep0']['media'], item['readout_error']['media']])
    dataFrame_T2.append([item['date'], item['T2']['media'], item['T1']['media'], item['prob_meas0_prep1']['media'], item['prob_meas1_prep0']['media'], item['readout_error']['media']])
    dataFrame_Prob0.append([item['date'], item['prob_meas0_prep1']['media'], item['T2']['media'], item['T1']['media'], item['prob_meas1_prep0']['media'], item['readout_error']['media']])
    dataFrame_Prob1.append([item['date'], item['prob_meas1_prep0']['media'], item['T2']['media'], item['prob_meas0_prep1']['media'], item['T1']['media'], item['readout_error']['media']])
    dataFrame_error.append([item['date'], item['readout_error']['media'], item['T2']['media'], item['prob_meas0_prep1']['media'], item['prob_meas1_prep0']['media'], item['T1']['media']])

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
