from pymongo import MongoClient
import csv

mongo_uri = "mongodb+srv://ivandelgadoalba:claveMongo@cluster0.pn3zcyq.mongodb.net/"
client = MongoClient(mongo_uri)

collection_name_Origen = "derivado"

db = client["TFG"]

def createDataFrame(machine):
    formatearNombre = machine.split("_")[1].capitalize()
    dataFrame_gates = [
        ['date', 'gate_error_1', 'gate_error_2']
    ]
    items = db[collection_name_Origen].find({"name": machine})
    for item in items:
      dataFrame_gates.append([item['date'], item['properties']['gates'][0]['mediana'], item['properties']['gates'][1]['mediana']])

    directorio = 'dataframes_gates/'
    nombre_archivo = directorio + 'dataframe_Gates' + formatearNombre + '.csv'

    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        
        escritor_csv = csv.writer(archivo_csv)
        
        for fila in dataFrame_gates:
            escritor_csv.writerow(fila)


maquinas = ["ibm_brisbane", "ibm_kyoto", "ibm_osaka"] 

for maquina in maquinas:
    createDataFrame(maquina)

print("Dataframes creados con exito")