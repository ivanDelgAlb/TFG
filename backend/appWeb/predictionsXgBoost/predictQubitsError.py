import numpy as np
import xgboost as xgb
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def predict(machine_name, data, depth):
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

    matrix_data = xgb.DMatrix(data_np)

    prediction = xgb_model.predict(matrix_data)

    predictions = add_date_and_calibration(prediction, data)

    return predictions

def add_date_and_calibration(errors, predictions):
    data_list = []
    date = datetime.now()

    for i, error in enumerate(errors):
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