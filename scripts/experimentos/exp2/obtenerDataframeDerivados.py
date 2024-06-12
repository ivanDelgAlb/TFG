from pymongo import MongoClient
import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv
import os

load_dotenv()

def dataFrame():
    mongo_uri_1 = "mongodb+srv://ivandelgadoalba:claveMongo@cluster0.pn3zcyq.mongodb.net/"
    client_1 = MongoClient(mongo_uri_1)
    collection_name_Origen = "derivado"
    db_1 = client_1["TFG"]
    data = db_1[collection_name_Origen].find({"name": "ibm_kyoto"})

    data_qubits = []


    qubits = [5, 10]
    depths = [5, 10]
    probabilities = [0.25, 0.75]

    for item in data:
        T1 = item['properties']['qubits'][0]['mediana']
        T2 = item['properties']['qubits'][1]['mediana']
        probMeas0Prep1 = item['properties']['qubits'][2]['mediana']
        probMeas1Prep0 = item['properties']['qubits'][3]['mediana']
        readout_error = item['properties']['qubits'][4]['mediana']
        for qubit in qubits:
            for depth in depths:
                for probability in probabilities:
                    data_qubits.append([T1, T2, probMeas0Prep1, probMeas1Prep0, readout_error, qubit, depth, probability, '', '', '', '', '', '', ''])


    df = pd.DataFrame(data_qubits, columns=['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_qubit_error', 'n_qubits', 'depth', 'probability', 't_gates', 'phase_gates', 'h_gates', 'cnot_gates', 'kullback_error', 'jensen-error', 'time'])


    directory = 'scripts/experimentos/exp2'

    df.to_csv(os.path.join(directory, f'dataframeKyoto_experiment_2.csv'), index=False)

    print("Extracción finalizada")


dataFrame()

print("Finalizado")
