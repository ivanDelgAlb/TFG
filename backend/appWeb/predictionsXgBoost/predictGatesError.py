import numpy as np
import xgboost as xgb
from datetime import datetime, timedelta

def predict(machine_name, data):
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

    file = 'backend/models_xgboost/xgboost_gate_model_' + formated_name + '.model'
    xgb_model = xgb.Booster()
    xgb_model.load_model(file)

    data_np = np.array(data)

    if data_np.ndim == 1:
        data_np = data_np.reshape(1, -1)

    matrix_data = xgb.DMatrix(data_np)

    errors = xgb_model.predict(matrix_data)

    predictions = add_date_and_calibration(errors, data)

    return predictions

def add_date_and_calibration(errors, predictions):
    data_list = []

    date = datetime.now()

    for i, error in enumerate(errors):
        error_dict = {"Date": date.strftime("%Y-%m-%d %H:%M:%S")}
        date = date + timedelta(hours=2)
        error_dict['divergence'] = error

        # Añadir las predicciones correspondientes
        if i < len(predictions):
            error_dict['gate_error_1'] = predictions[i][0][0]
            error_dict['gate_error_2'] = predictions[i][0][1]

        data_list.append(error_dict)

    return data_list