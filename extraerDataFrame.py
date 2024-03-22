from pymongo import MongoClient
import csv

mongo_uri = "mongodb+srv://Marina:mongoTFG@tfg.qet3gme.mongodb.net/"
client = MongoClient(mongo_uri)

collection_name_Origen = "dataFrame"

db = client["TFG"]

datos = db[collection_name_Origen].find({'name': 'ibm_brisbane'})

dataFrame = [
    ['ds', 'y']
]

for item in datos[0]['data']:
    dataFrame.append([item['date'], item['T1']['media']])

nombre_archivo = 'datos.csv'

with open(nombre_archivo, 'w', newline='') as archivo_csv:
    
    escritor_csv = csv.writer(archivo_csv)
    
    for fila in dataFrame:
        escritor_csv.writerow(fila)
