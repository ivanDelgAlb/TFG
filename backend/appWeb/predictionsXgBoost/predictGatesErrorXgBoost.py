import numpy as np
import xgboost as xgb
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv

load_dotenv()

def predict(machine_name, data, type):
    """
    Predicts for the selected machine the error associated to the provided data
    :param machine_name: The name of the quantum machine
    :param data: The inputs for the model
    :type machine_name: String
    :type data: list of lists of lists
    :return: The predicted values
    :rtype: list of floats
    """
    formated_name = machine_name.split(" ")[1].capitalize()

    if os.getenv("DEPLOYMENT") == 'localhost': models_directory = os.path.join(os.getenv("PATH_FILE"), 'models_xgboost/')
    else: models_directory = os.path.join(os.environ['PWD'], 'models_xgboost/')

    file = models_directory + 'xgboost_gate_model_' + formated_name + '.model'
    xgb_model = xgb.Booster()
    xgb_model.load_model(file)

    data_np = np.array(data)

    if data_np.ndim == 1:
        data_np = data_np.reshape(1, -1)

    if type == 'calibration' and data_np.ndim == 3:
        data_np = data_np.reshape(data_np.shape[0], -1)

    matrix_data = xgb.DMatrix(data_np)

    errors = xgb_model.predict(matrix_data)

    predictions = add_date_and_calibration(errors, data, type)

    return predictions

def add_date_and_calibration(errors, predictions, type):
    data_list = []

    date = datetime.now()

    for i, error in enumerate(errors):
        if error < 0: error = 0
        elif error > 1: error = 1
        else: error   
        error_dict = {"Date": date.strftime("%Y-%m-%d %H:%M:%S")}
        date = date + timedelta(hours=2)
        error_dict['divergence'] = error

        if i < len(predictions):
            if type == 'calibration':
                error_dict['error_gate_1_qubit'] = predictions[i][0][1]
                error_dict['error_gate_2_qubit'] = predictions[i][0][2]
            else:
                error_dict['error_gate_1_qubit'] = predictions[i][0]
                error_dict['error_gate_2_qubit'] = predictions[i][1]

        data_list.append(error_dict)

    return data_list