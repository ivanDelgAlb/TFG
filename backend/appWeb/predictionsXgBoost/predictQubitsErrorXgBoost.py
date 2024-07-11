import numpy as np
import xgboost as xgb
from datetime import datetime, timedelta
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def predict(machine_name, data, type):
    """
    Predicts for the selected machine the error associated to the provided data
    :param machine_name: The name of the quantum machine
    :param data: The inputs for the model
    :type machine_name: str
    :type data: list of lists of lists
    :param depth: Depth value to filter the dataset
    :type depth: int
    :return: The predicted values
    :rtype: list of floats
    """

    formated_name = machine_name.split(" ")[1].capitalize()

    if os.getenv("DEPLOYMENT") == 'localhost': models_directory = os.path.join(os.getenv("PATH_FILE"), 'models_xgboost/')
    else: models_directory = os.path.join(os.environ['PWD'], 'models_xgboost/')
    
    file = models_directory + 'xgboost_qubit_model_' + formated_name + '.model'
    xgb_model = xgb.Booster()
    xgb_model.load_model(file)

    data_np = np.array(data)

    if data_np.ndim == 1:
        data_np = data_np.reshape(1, -1)

    columns_to_normalize = ["T1", "T2", "Prob0", "Prob1", "Error"]

    # Crear DataFrame con los datos y nombres de columnas
    columns = ["T1", "T2", "Prob0", "Prob1", "Error", "n_qubits", "depth", "t_gates", "phase_gates", "h_gates", "cnot_gates"]
    if type == 'calibration' : df = pd.DataFrame(data_np[0], columns=columns)
    else : df = pd.DataFrame(data_np, columns=columns)

    # Asegurar que las columnas a normalizar sean numéricas
    for col in columns_to_normalize:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Normalizar las columnas especificadas
    X = df.drop(['n_qubits', 'depth', 't_gates', 'phase_gates', 'h_gates', 'cnot_gates'], axis=1)

    #X_normalizado = X.apply(lambda fila: (fila - fila.min()) / (fila.max() - fila.min()), axis=1)
    X_normalizado = X

    X_normalizado['n_qubits'] = df['n_qubits']
    X_normalizado['depth'] = df['depth']
    X_normalizado['t_gates'] = df['t_gates']
    X_normalizado['phase_gates'] = df['phase_gates']
    X_normalizado['h_gates'] = df['h_gates']
    X_normalizado['cnot_gates'] = df['cnot_gates']

    # Convertir el DataFrame normalizado de vuelta a numpy array
    data_np = X_normalizado.values

    matrix_data = xgb.DMatrix(data_np)

    prediction = xgb_model.predict(matrix_data)

    if type == 'calibration': predictions = add_date_and_calibration(prediction, data[0])
    else : predictions = add_date_and_calibration(prediction, data)

    return predictions

def add_date_and_calibration(errors, predictions):
    data_list = []
    date = datetime.now()

    for i, error in enumerate(errors):
        if error < 0: error = 0
        elif error > 1: error = 1
        else: error   
        error_dict = {"Date": date.strftime("%Y-%m-%d %H:%M:%S")}
        date += timedelta(hours=2)
        error_dict['divergence'] = error

        if i < len(predictions):
            error_dict['T1'] = predictions[i][0]
            error_dict['T2'] = predictions[i][1]
            error_dict['Prob0'] = predictions[i][2]
            error_dict['Prob1'] = predictions[i][3]
            error_dict['Error'] = predictions[i][4]

        data_list.append(error_dict)

    return data_list