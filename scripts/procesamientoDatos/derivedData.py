from pymongo import MongoClient
import statistics

import os
from dotenv import load_dotenv

load_dotenv()

origin_mongo_uri = os.getenv("MONGO_URI_MARINA_PART1")
origin_client = MongoClient(origin_mongo_uri)

destination_mongo_uri = os.getenv("MONGO_URI_IVAN_PART1")
destination_client = MongoClient(destination_mongo_uri)

destination_collection_name = "derivado"
origin_collection_name = "data"

db_Origen = origin_client["TFG"]
db_Destino = destination_client["TFG"]


def calculate_mean(data, nqubit, attribute):
    mean = 0
    count = 0

    for datum in data:
        if nqubit > 0:
            if len(datum['qubits']) == nqubit:
                for gate in datum['parameters']:
                    if gate['name'] == 'gate_error':
                        mean += gate['value']
                        count += 1
        else:
            for qubit in datum:
                if qubit['name'] == attribute:
                    mean += qubit['value']
                    count += 1

    if count > 0:
        mean = mean / count
    
    return mean


def calculate_median(data, nqubit, attribute):
    values = []

    for datum in data:
        if nqubit > 0:
            if len(datum['qubits']) == nqubit:
                for gate in datum['parameters']:
                    if gate['name'] == attribute:
                        values.append(gate['value'])
        else:
            for qubit in datum:
                if qubit['name'] == attribute:
                    values.append(qubit['value'])
    values.sort()
    n = len(values)
    
    if n % 2 == 0:
        median = (values[n//2 - 1] + values[n//2]) / 2
    else:
        median = values[n//2]

    return median


def calculate_deviation(data, nqubit, attribute):
    values = []

    for datum in data:
        if nqubit > 0:
            if len(datum['qubits']) == nqubit:
                for gate in datum['parameters']:
                    if gate["name"] == attribute:
                        values.append(gate['value'])
        else:
            for qubit in datum:
                if qubit["name"] == attribute:
                    values.append(qubit['value'])

    if len(values) < 2:
        return None

    deviation = statistics.stdev(values)
    return deviation

    
data = db_Origen[origin_collection_name].find()

for datum in data:

    qubits = datum['properties']['qubits']
    derived_qubits = []

    gates = datum["properties"]["gates"]
    derived_gates = []
        
    attributes = ["T1", "T2", "prob_meas0_prep1", "prob_meas1_prep0", "readout_error", "gate_error", "gate_length"]
    nqubits = [1, 2]

    for attribute in attributes:

        if attribute != "gate_error" and attribute != "gate_length":

            document = {
                "name": attribute,
                "media": calculate_mean(qubits, -1, attribute),
                "mediana": calculate_median(qubits, -1, attribute),
                "desviacion": calculate_deviation(qubits, -1, attribute)
            }

            derived_qubits.append(document)
        
        else:

            for nqubit in nqubits:
                document = {
                    "name": attribute,
                    "nºqubits": nqubit,
                    "media": calculate_mean(gates, nqubit, attribute),
                    "mediana": calculate_median(gates, nqubit, attribute),
                    "desviacion": calculate_deviation(gates, nqubit, attribute)
                }
                derived_gates.append(document)

    datum['properties']['qubits'] = derived_qubits
    datum['properties']['gates'] = derived_gates

    datum['properties'].pop('general', None)
    datum['properties'].pop('general_qlists', None)
    datum.pop('configuration', None)

    collection = db_Destino[destination_collection_name]

    collection.insert_one(datum)
    print(f"Data inserted successfully. Date: {datum['date']}, machine: {datum['name']}")
    

print("All data has been inserted correctly")
