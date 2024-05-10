import pandas as pd
from pymongo import MongoClient
from calculateNoiseError import calculate_configuration_gate_error
from generateCircuit import generate_circuit
import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from qiskit_ibm_runtime import QiskitRuntimeService
import csv


def generate_dataframe_gates():
    dataframe = [["gate_error_one_qubit", "gate_error_two_qubit", "divergence"]]
    mongo_uri = "mongodb+srv://ivandelgadoalba:claveMongo@cluster0.pn3zcyq.mongodb.net/"
    client = MongoClient(mongo_uri)

    collection_name_Origen = "derivado"

    db = client["TFG"]
    datos = db[collection_name_Origen].find({"name": "ibm_brisbane"})
    service = QiskitRuntimeService(channel='ibm_quantum',
                                   token='8744729d1df2b54f6d544d5e4d49e3c1929372023734570e3db2f4a5568cf68ce8140213570c3a79c13548a13a0106bd3cd23c16578ef36b8e0139407b93d67a')
    circuit = generate_circuit(5, 5)
    contador = 0

    for item in datos:

        if contador == 50:
            break

        fila = []

        gate_error_one_qubit = item['properties']['gates'][0]['mediana']
        gate_error_two_qubit = item['properties']['gates'][1]['mediana']

        backend = service.get_backend("ibm_brisbane")

        divergence = calculate_configuration_gate_error(circuit, backend, gate_error_one_qubit, gate_error_two_qubit)

        fila.extend([gate_error_one_qubit, gate_error_two_qubit, divergence])

        dataframe.append(fila)
        contador += 1

    nombre_archivo = 'dataframe_gates_' + 'Brisbane' + '.csv'

    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerows(dataframe)

    print("El archivo {} ha sido creado exitosamente.".format(nombre_archivo))


def create_model(machine_name):
    """
    Creates a xgBoost model from an existing dataframe
    :param machine_name: The name of the quantum machine
    :type machine_name: String
    :return: None
    """
    formated_name = machine_name.split("_")[1].capitalize()

    columns = ["gate_error_one_qubit", "gate_error_two_qubit", "divergence"]

    dataset = pd.read_csv('dataframes_xgboost/dataframe_gates_' + formated_name + '.csv', names=columns)
    dataset['gate_error_one_qubit'] = pd.to_numeric(dataset['gate_error_one_qubit'], errors='coerce')
    dataset['gate_error_two_qubit'] = pd.to_numeric(dataset['gate_error_two_qubit'], errors='coerce')
    dataset['divergence'] = pd.to_numeric(dataset['divergence'], errors='coerce')

    train_set, test_set = train_test_split(dataset, test_size=0.2)
    train_set = train_set.dropna(subset=['divergence'])

    x_train = train_set.drop("divergence", axis=1)
    y_train = train_set["divergence"]
    x_test = test_set.drop("divergence", axis=1)
    y_test = test_set["divergence"]

    dtrain = xgb.DMatrix(x_train, label=y_train)
    dtest = xgb.DMatrix(x_test, label=y_test)

    params = {
        "objective": "reg:squarederror",
        "eval_metric": "rmse"
    }

    num_rounds = 100
    xgb_model = xgb.train(params, dtrain, num_rounds)

    predictions = xgb_model.predict(dtest)

    rmse = mean_squared_error(y_test, predictions, squared=False)
    print("RMSE:", rmse)

    file = 'models_xgboost/xgboost_gate_model_' + formated_name + '.model'
    xgb_model.save_model(file)
    print("Model created")

    '''
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, predictions, color='blue', label='Datos reales vs Predicciones')
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
    plt.xlabel('Datos reales')
    plt.ylabel('Predicciones')
    plt.title('Predicciones vs Datos reales')
    plt.legend()
    plt.show()
    '''


def predict(machine_name, data):
    """
    Predicts for the selected machine the error associated to the provided data
    :param machine_name: The name of the quantum machine
    :param data: The inputs for the model
    :type machine_name: String
    :type data: list of lists
    :return: The predicted value
    :rtype: list(float)
    """
    formated_name = machine_name.split("_")[1].capitalize()

    file = 'models_xgboost/xgboost_gate_model_' + formated_name + '.model'
    xgb_model = xgb.Booster()
    xgb_model.load_model(file)

    data_np = np.array(data)

    matrix_data = xgb.DMatrix(data_np)

    prediction = xgb_model.predict(matrix_data)

    return prediction


# generate_dataframe_gates()
# create_model("ibm_brisbane")
prediction = predict("ibm_brisbane", [[0.00013306438200978542, 0.004955224553499893]])
print(prediction)
