from pymongo import MongoClient
import csv

mongo_uri = 'mongodb+srv://Marina:mongoTFG@tfg.qet3gme.mongodb.net/'
client = MongoClient(mongo_uri)

collection_name_Origen = 'dataFrame'

db = client['TFG']

datos = db[collection_name_Origen].find({'name': 'ibm_brisbane'})

dataFrame = [
    ['ds', 'y', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error']
]

for item in datos[0]['data']:
    dataFrame.append([item['date'], item['T1']['media'], item['T2']['media'], item['prob_meas0_prep1']['media'], item['prob_meas1_prep0']['media'], item['readout_error']['media']
                    ])

nombre_archivo = 'datos.csv'

with open(nombre_archivo, 'w', newline='') as archivo_csv:
    
    escritor_csv = csv.writer(archivo_csv)
    
    for fila in dataFrame:
        escritor_csv.writerow(fila)
