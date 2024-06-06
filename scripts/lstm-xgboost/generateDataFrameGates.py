from pymongo import MongoClient
import csv

mongo_uri = "mongodb+srv://ivandelgadoalba:claveMongo@cluster0.pn3zcyq.mongodb.net/"
client = MongoClient(mongo_uri)

collection_name_Origen = "derivado"

db = client["TFG"]

def createDataFrame(machine):
    formated_name = machine.split("_")[1].capitalize()
    dataFrame_gates = [
        ['date', 'gate_error_1', 'gate_error_2']
    ]
    items = db[collection_name_Origen].find({"name": machine})
    for item in items:
      dataFrame_gates.append([item['date'], item['properties']['gates'][0]['mediana'], item['properties']['gates'][1]['mediana']])

    directory = 'backend/dataframes_gates/'

    file_name = directory + 'dataframe_Gates' + formated_name + '.csv'

    with open(file_name, 'w', newline='') as csv_file:
        
        csv_writer = csv.writer(csv_file)
        
        for row in dataFrame_gates:
            csv_writer.writerow(row)


machines = ["ibm_brisbane", "ibm_kyoto", "ibm_osaka"] 

for machine in machines:
    createDataFrame(machine)

("Dataframes created")