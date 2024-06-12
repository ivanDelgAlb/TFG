from pymongo import MongoClient
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

mongo_uri_1 = os.getenv("MONGO_URI_IVAN_PART1")
client_1 = MongoClient(mongo_uri_1)
collection_name_Origen = "derivado"
db_1 = client_1["TFG"]

dataframe_qubits = [
    ['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error']
]

dataframe_gates = [
    ['date', 'gate_error_one_qubit', 'gate_error_two_qubit']
]

def normalised_qubits(machine_name):
    formated_name = machine_name.split("_")[1].capitalize()
    data_qubits = []
    data = db_1[collection_name_Origen].find({"name": machine_name})

    for item in data:
        T1 = item['properties']['qubits'][0]['mediana']
        T2 = item['properties']['qubits'][1]['mediana']
        probMeas0Prep1 = item['properties']['qubits'][2]['mediana']
        probMeas1Prep0 = item['properties']['qubits'][3]['mediana']
        readout_error = item['properties']['qubits'][4]['mediana']

        data_qubits.append([T1, T2, probMeas0Prep1, probMeas1Prep0, readout_error])

    df_qubits = pd.DataFrame(data_qubits, columns=['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error'])

    file_name = 'backend/dataframes_qubits/'
    scaler = MinMaxScaler()

    df_qubits.iloc[:, :] = scaler.fit_transform(df_qubits)
    joblib.dump(scaler, 'backend/dataframes_qubits/scalerQubits' + formated_name + '.pkl')

    df_qubits.to_csv(os.path.join(file_name, f'dataframeQubits{formated_name}.csv'), index=False)

    ("The file {} has been created.".format(file_name))


def generate_dataframe_gates(machine_name):
    formated_name = machine_name.split("_")[1].capitalize()
    data_gates = []
    data = db_1[collection_name_Origen].find({"name": machine_name})

    for item in data:
        date = item['date']
        gate_error_one_qubit = item['properties']['gates'][0]['mediana']
        gate_error_two_qubit = item['properties']['gates'][1]['mediana']

        data_gates.append([date, gate_error_one_qubit, gate_error_two_qubit])

    df_gates = pd.DataFrame(data_gates, columns=['date', 'gate_error_1', 'gate_error_2'])

    file_name = 'backend/dataframes_gates/'

    df_gates.to_csv(os.path.join(file_name, f'dataframe_Gates{formated_name}.csv'), index=False)

    ("The file {} has been created.".format(file_name))


normalised_qubits("ibm_brisbane")
normalised_qubits("ibm_kyoto")
normalised_qubits("ibm_osaka")
generate_dataframe_gates("ibm_brisbane")
generate_dataframe_gates("ibm_kyoto")
generate_dataframe_gates("ibm_osaka")
