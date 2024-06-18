from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

origin_mongo_uri = os.getenv("MONGO_URI_MARINA_PART1")
destination_mongo_uri = os.getenv("MONGO_URI_IVAN_PART1")
origin_client = MongoClient(origin_mongo_uri)
destination_client = MongoClient(destination_mongo_uri)

destination_collection_name = "derivado"
origin_collection_name = "data"

origin_db = origin_client["TFG"]
destination_db = destination_client["TFG"]

destination_db[destination_collection_name].drop()
print("Collection deleted successfully")

data = origin_db[origin_collection_name].find()
for datum in data:

    qubits = datum['properties']['qubits']

    qubits_without_attributes = []

    for qubit in qubits:
        qubit_without_attributes = []
        for q in qubit:
            if q['name'] != 'frequency' and q['name'] != 'anharmonicity':
                qubit_without_attributes.append(q)
        qubits_without_attributes.append(qubit_without_attributes)

    datum['properties']['qubits'] = qubits_without_attributes
    
    datum['properties'].pop('general', None)
    datum['properties'].pop('general_qlists', None)
    datum.pop('configuration', None)
    
    collection = destination_db[destination_collection_name]
    collection.insert_one(datum)

print("The data has been filtered successfully")
