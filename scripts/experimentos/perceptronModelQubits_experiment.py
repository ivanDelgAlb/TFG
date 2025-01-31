import pandas as pd
from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import Dense
from calculateNoiseError import calculate_configuration_qubit_error
from qiskit_ibm_runtime import QiskitRuntimeService
from sklearn.model_selection import train_test_split
from keras.models import load_model
from pymongo import MongoClient
import csv
import math


def extraer_dataframe_normalizado(circuit, fake_backend):
    mongo_uri = "mongodb+srv://ivandelgadoalba:claveMongo@cluster0.pn3zcyq.mongodb.net/"
    client = MongoClient(mongo_uri)

    collection_name_Origen = "derivado"

    db = client["TFG"]

    service = QiskitRuntimeService(channel='ibm_quantum',
                                   token='8744729d1df2b54f6d544d5e4d49e3c1929372023734570e3db2f4a5568cf68ce8140213570c3a79c13548a13a0106bd3cd23c16578ef36b8e0139407b93d67a')

    dataFrame = [
        ['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error', 'divergence']
    ]

    

    def normalized(nombre_maquina):
        formatearNombre = nombre_maquina.split("_")[1].capitalize()

        datos = db[collection_name_Origen].find({"name": nombre_maquina})
        contador = 0

        for item in datos:

            if contador == 40:
                break

            fila = []
            fake_backend = service.get_backend('ibm_brisbane')
            date = item['date']
            T1 = item['properties']['qubits'][0]['mediana']
            T2 = item['properties']['qubits'][1]['mediana']
            probMeas0Prep1 = item['properties']['qubits'][2]['mediana']
            probMeas1Prep0 = item['properties']['qubits'][3]['mediana']
            readout_error = item['properties']['qubits'][4]['mediana']

            divergence = calculate_configuration_qubit_error(circuit, fake_backend, T1, T2, probMeas0Prep1, probMeas1Prep0, readout_error)
            ("Divergencia calculada :)")
            fila_min = min(T1, T2, probMeas0Prep1, probMeas1Prep0, readout_error)
            fila_max = max(T1, T2, probMeas0Prep1, probMeas1Prep0, readout_error)

            T1_norm = (T1 - fila_min) / (fila_max - fila_min)
            T2_norm = (T2 - fila_min) / (fila_max - fila_min)
            probMeas0Prep1_norm = (probMeas0Prep1 - fila_min) / (fila_max - fila_min)
            probMeas1Prep0_norm = (probMeas1Prep0 - fila_min) / (fila_max - fila_min)
            readout_error_norm = (readout_error - fila_min) / (fila_max - fila_min)

            fila.extend([T1_norm, T2_norm, probMeas0Prep1_norm, probMeas1Prep0_norm, readout_error_norm, divergence])

            dataFrame.append(fila)
            contador += 1

        nombre_archivo = 'dataframes_neuralProphet/dataframe_'+ formatearNombre + '.csv'

        with open(nombre_archivo, 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerows(dataFrame)

        ("El archivo {} ha sido creado exitosamente.".format(nombre_archivo))

    normalized("ibm_brisbane")


def create_model(machine, X_train, X_test, y_train, y_test):
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='linear'))

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)
    print("Metricas: ", model.get_metrics_result())
    mse, mae = model.evaluate(X_test, y_test)
    print(f"Error cuadrático medio ({machine}):", math.sqrt(mse))

    directory = f'scripts/experimentos/experiment_perceptron_qubits_{machine}.h5'
    model.save(directory)



def predict(machine, X_test, y_test):
    directory = 'backend/models_perceptron/model_qubits_' + machine + '.h5'
    model = load_model(directory)
    reconstructed_data_X = model.predict(X_test)

    for i in range(len(X_test)):
        original_data_y = y_test.iloc[i]
        reconstructed_sample_X = reconstructed_data_X[i]
        print("Original_Y:", original_data_y)
        print("Reconstruido_X:", reconstructed_sample_X)
        print("\n")
'''
circuit = generate_circuit(20, 5)
service = QiskitRuntimeService(channel='ibm_quantum',
                                   token='8744729d1df2b54f6d544d5e4d49e3c1929372023734570e3db2f4a5568cf68ce8140213570c3a79c13548a13a0106bd3cd23c16578ef36b8e0139407b93d67a')
fake_backend = service.get_backend('ibm_brisbane')

extraer_dataframe_normalizado(circuit, fake_backend)

'''

machines = ["Brisbane", "Kyoto", "Osaka"]
for machine in machines:
    directory = 'scripts/experimentos/exp1/dataframe_experiment_qubit_' + machine + ".csv"
    dataFrame = pd.read_csv(directory)

    filas_filtradas = dataFrame[(dataFrame['jensen-error'].notna())]

    X = filas_filtradas.drop(['n_qubits', 'depth', 't_gates', 'phase_gates', 'h_gates', 'cnot_gates', 'kullback_error', 'jensen-error'], axis=1)

    X_normalizado = X.apply(lambda fila: (fila - fila.min()) / (fila.max() - fila.min()), axis=1)

    X_normalizado['n_qubits'] = filas_filtradas['n_qubits']
    X_normalizado['depth'] = filas_filtradas['depth']
    X_normalizado['t_gates'] = filas_filtradas['t_gates']
    X_normalizado['phase_gates'] = filas_filtradas['phase_gates']
    X_normalizado['h_gates'] = filas_filtradas['h_gates']
    X_normalizado['cnot_gates'] = filas_filtradas['cnot_gates']

    y = filas_filtradas['jensen-error']

    X_train, X_test, y_train, y_test = train_test_split(X_normalizado, y, test_size=0.2, random_state=42)

    create_model(machine, X_train, X_test, y_train, y_test)

    #predict(machine, X_test, y_test)

print("Models created")

#predict()

