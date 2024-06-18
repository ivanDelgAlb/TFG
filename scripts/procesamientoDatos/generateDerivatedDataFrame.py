from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI_MARINA_PART1")
client = MongoClient(mongo_uri)

destination_collection_name = "dataFrame"
origin_collection_name = "derivado"

db = client["TFG"]

db[destination_collection_name].drop()
print("Collection deleted successfully")

data = db[origin_collection_name].find()


for document in data:
    machine_name = document['name']
    existent_document = db[destination_collection_name].find_one({"name": machine_name})
    if existent_document:
        new_data = {
            "date": document['date'],
            "T1": document['properties']['qubits'][0],
            "T2": document['properties']['qubits'][1],
            "prob_meas0_prep1": document['properties']['qubits'][2],
            "prob_meas1_prep0": document['properties']['qubits'][3],
            "readout_error": document['properties']['qubits'][4]
        }

        db[destination_collection_name].update_one({"_id": existent_document["_id"]}, {"$push": {"data": new_data}})
        print(f"Data updated for {machine_name}")
    else:
        data = {
            "name": machine_name,
            "data": [{
                "date": document['date'],
                "T1": document['properties']['qubits'][0],
                "T2": document['properties']['qubits'][1],
                "prob_meas0_prep1": document['properties']['qubits'][2],
                "prob_meas1_prep0": document['properties']['qubits'][3],
                "readout_error": document['properties']['qubits'][4]
            }]
        }
        db[destination_collection_name].insert_one(data)
        print(f"New document created for {machine_name}")

print("Iteration over the db has been completed")
