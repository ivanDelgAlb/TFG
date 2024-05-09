import pandas as pd
from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import Dense
from generateCircuit import generate_circuit
from calculateNoiseError import calculate_configuration_qubit_error
from qiskit_ibm_runtime import QiskitRuntimeService
from sklearn.model_selection import train_test_split
from keras.models import load_model

from pymongo import MongoClient
import csv



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
            print("Divergencia calculada :)")
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

        nombre_archivo = 'dataframes/dataframe_'+ formatearNombre + '.csv'

        with open(nombre_archivo, 'w', newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerows(dataFrame)

        print("El archivo {} ha sido creado exitosamente.".format(nombre_archivo))

    normalized("ibm_brisbane")

'''
circuit = generate_circuit(4, 5)
service = QiskitRuntimeService(channel='ibm_quantum',
                                   token='8744729d1df2b54f6d544d5e4d49e3c1929372023734570e3db2f4a5568cf68ce8140213570c3a79c13548a13a0106bd3cd23c16578ef36b8e0139407b93d67a')
fake_backend = service.get_backend('ibm_brisbane')

extraer_dataframe_normalizado(circuit, fake_backend)
'''
# Cargar el dataframe desde el archivo CSV
def create_model():
    # Construir el modelo de perceptrón multicapa
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='linear'))

    # Compilar el modelo
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    # Entrenar el modelo
    model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

    # Evaluar el rendimiento del modelo en el conjunto de prueba
    mse, mae = model.evaluate(X_test, y_test)
    print("Error cuadrático medio:", mse)
    print("Error absoluto medio:", mae)

    # Guardar el modelo
    model.save('models_perceptron/model_Brisbane.h5')



def predict():
    # Reconstrucción de datos de prueba
    # Cargar el modelo
    model = load_model('models_perceptron/model_Brisbane.h5')
    reconstructed_data_X = model.predict(X_test)

    # Comparación entre datos originales y datos reconstruidos
    for i in range(len(X_test)):
        original_data_y = y_test.iloc[i]  # Accede al valor de la etiqueta i del DataFrame y_test
        reconstructed_sample_X = reconstructed_data_X[i]  # Predicción reconstruida para la muestra i de X
        print("Original_Y:", original_data_y)
        print("Reconstruido_X:", reconstructed_sample_X)
        print("\n")


dataFrame = pd.read_csv('dataframes/dataframe_Brisbane.csv')

X = dataFrame.drop('divergence', axis=1)  # Características
y = dataFrame['divergence']  # Etiqueta (divergencia)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#create_model()
predict()

