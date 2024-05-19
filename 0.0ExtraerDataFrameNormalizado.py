
from pymongo import MongoClient
import csv
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

mongo_uri = "mongodb+srv://ivandelgadoalba:claveMongo@cluster0.pn3zcyq.mongodb.net/"
client = MongoClient(mongo_uri)

collection_name_Origen = "derivado"

db = client["TFG"]

dataframe_qubits = [
    ['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error']
]

dataframe_gates = [
    ['date', 'gate_error_one_qubit', 'gate_error_two_qubit']
]

def normalised_qubits(nombre_maquina):
    formatearNombre = nombre_maquina.split("_")[1].capitalize()
    data_qubits = []
    datos = db[collection_name_Origen].find({"name": nombre_maquina})

    for item in datos:
        T1 = item['properties']['qubits'][0]['mediana']
        T2 = item['properties']['qubits'][1]['mediana']
        probMeas0Prep1 = item['properties']['qubits'][2]['mediana']
        probMeas1Prep0 = item['properties']['qubits'][3]['mediana']
        readout_error = item['properties']['qubits'][4]['mediana']

        data_qubits.append([T1, T2, probMeas0Prep1, probMeas1Prep0, readout_error])
        
    df_qubits = pd.DataFrame(data_qubits, columns=['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error'])

    nombre_archivo = 'dataframes_qubits/'

    scaler = MinMaxScaler()

    df_qubits.iloc[:, 1:] = scaler.fit_transform(df_qubits.iloc[:, 1:])
    joblib.dump(scaler, 'dataframes_qubits/scalerQubits' + formatearNombre + '.pkl')

    df_qubits.to_csv(os.path.join(nombre_archivo, f'dataframeQubits{formatearNombre}.csv'), index=False)

    print("El archivo {} ha sido creado exitosamente.".format(nombre_archivo))


def generate_dataframe_gates(nombre_maquina):
    formatearNombre = nombre_maquina.split("_")[1].capitalize()
    data_gates = []
    datos = db[collection_name_Origen].find({"name": nombre_maquina})

    for item in datos:
        date = item['date']
        gate_error_one_qubit = item['properties']['gates'][0]['mediana']
        gate_error_two_qubit = item['properties']['gates'][1]['mediana']

        data_gates.append([date, gate_error_one_qubit, gate_error_two_qubit])

    df_gates = pd.DataFrame(data_gates, columns=['date', 'gate_error_1', 'gate_error_2'])

    nombre_archivo = 'backend/dataframes_gates/'
    scaler = MinMaxScaler()

    df_gates.iloc[:, 1:] = scaler.fit_transform(df_gates.iloc[:, 1:])
    joblib.dump(scaler, 'backend/dataframes_gates/scalerGates' + formatearNombre + '.pkl')

    df_gates.to_csv(os.path.join(nombre_archivo, f'dataframe_Gates{formatearNombre}.csv'), index=False)

    print("El archivo {} ha sido creado exitosamente.".format(nombre_archivo))


#normalised_qubits("ibm_brisbane")
#normalised_qubits("ibm_kyoto")
#normalised_qubits("ibm_osaka")
generate_dataframe_gates("ibm_brisbane")
generate_dataframe_gates("ibm_kyoto")
generate_dataframe_gates("ibm_osaka")
