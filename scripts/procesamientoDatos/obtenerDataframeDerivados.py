from pymongo import MongoClient
import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os

def dataFrame(nombre_maquina):
    formatearNombre = nombre_maquina.split("_")[1].capitalize()
    mongo_uri_1 = os.getenv("MONGO_URI_IVAN_PART1")
    mongo_uri_2 = os.getenv("MONGO_URI_IVAN_PART2")
    client_1 = MongoClient(mongo_uri_1)
    client_2 = MongoClient(mongo_uri_2)
    collection_name_Origen = "derivado"
    db_1 = client_1["TFG"]
    db_2 = client_2["TFG"]
    datos = db_1[collection_name_Origen].find({"name": nombre_maquina})

    data_T1 = []
    data_T2 = []
    data_Prob0 = []
    data_Prob1 = []
    data_error = []

    for item in datos:
        date = item['date']
        T1 = item['properties']['qubits'][0]['mediana']
        T2 = item['properties']['qubits'][1]['mediana']
        probMeas0Prep1 = item['properties']['qubits'][2]['mediana']
        probMeas1Prep0 = item['properties']['qubits'][3]['mediana']
        readout_error = item['properties']['qubits'][4]['mediana']

        data_T1.append([date, T1, T2, probMeas0Prep1, probMeas1Prep0, readout_error])
        data_T2.append([date, T2, T1, probMeas0Prep1, probMeas1Prep0, readout_error])
        data_Prob0.append([date, probMeas0Prep1, T1, T2, probMeas1Prep0, readout_error])
        data_Prob1.append([date, probMeas1Prep0, T1, T2, probMeas0Prep1, readout_error])
        data_error.append([date, readout_error, T1, T2, probMeas0Prep1, probMeas1Prep0])
    
    datos = db_2[collection_name_Origen].find({"name": nombre_maquina})

    for item in datos:
        date = item['date']
        T1 = item['properties']['qubits'][0]['mediana']
        T2 = item['properties']['qubits'][1]['mediana']
        probMeas0Prep1 = item['properties']['qubits'][2]['mediana']
        probMeas1Prep0 = item['properties']['qubits'][3]['mediana']
        readout_error = item['properties']['qubits'][4]['mediana']

        data_T1.append([date, T1, T2, probMeas0Prep1, probMeas1Prep0, readout_error])
        data_T2.append([date, T2, T1, probMeas0Prep1, probMeas1Prep0, readout_error])
        data_Prob0.append([date, probMeas0Prep1, T1, T2, probMeas1Prep0, readout_error])
        data_Prob1.append([date, probMeas1Prep0, T1, T2, probMeas0Prep1, readout_error])
        data_error.append([date, readout_error, T1, T2, probMeas0Prep1, probMeas1Prep0])

    df_T1 = pd.DataFrame(data_T1, columns=['ds', 'y', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error'])
    df_T2 = pd.DataFrame(data_T2, columns=['ds', 'y', 'T1', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error'])
    df_Prob0 = pd.DataFrame(data_Prob0, columns=['ds', 'y', 'T1', 'T2', 'probMeas1Prep0', 'readout_error'])
    df_Prob1 = pd.DataFrame(data_Prob1, columns=['ds', 'y', 'T1', 'T2', 'probMeas0Prep1', 'readout_error'])
    df_error = pd.DataFrame(data_error, columns=['ds', 'y', 'T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0'])

    scaler = MinMaxScaler()
    df_T1.iloc[:, 1:] = scaler.fit_transform(df_T1.iloc[:, 1:])
    joblib.dump(scaler, 'backend/dataframes_neuralProphet/scalerT1' + formatearNombre + '.pkl')

    scaler = MinMaxScaler()
    df_T2.iloc[:, 1:] = scaler.fit_transform(df_T2.iloc[:, 1:])
    joblib.dump(scaler, 'backend/dataframes_neuralProphet/scalerT2' + formatearNombre + '.pkl')

    scaler = MinMaxScaler()
    df_Prob0.iloc[:, 1:] = scaler.fit_transform(df_Prob0.iloc[:, 1:])
    joblib.dump(scaler, 'backend/dataframes_neuralProphet/scalerProb0' + formatearNombre + '.pkl')

    scaler = MinMaxScaler()
    df_Prob1.iloc[:, 1:] = scaler.fit_transform(df_Prob1.iloc[:, 1:])
    joblib.dump(scaler, 'backend/dataframes_neuralProphet/scalerProb1' + formatearNombre + '.pkl')

    scaler = MinMaxScaler()    
    df_error.iloc[:, 1:] = scaler.fit_transform(df_error.iloc[:, 1:])
    joblib.dump(scaler, 'backend/dataframes_neuralProphet/scalerError' + formatearNombre + '.pkl')


    directorio = 'backend/dataframes_neuralProphet/'

    df_T1.to_csv(os.path.join(directorio, f'dataframeT1{formatearNombre}.csv'), index=False)
    df_T2.to_csv(os.path.join(directorio, f'dataframeT2{formatearNombre}.csv'), index=False)
    df_Prob0.to_csv(os.path.join(directorio, f'dataframeProb0{formatearNombre}.csv'), index=False)
    df_Prob1.to_csv(os.path.join(directorio, f'dataframeProb1{formatearNombre}.csv'), index=False)
    df_error.to_csv(os.path.join(directorio, f'dataframeError{formatearNombre}.csv'), index=False)

    print("Extracción finalizada")


maquinas = ["ibm_brisbane", "ibm_kyoto", "ibm_osaka"] 

for maquina in maquinas:
    dataFrame(maquina)
