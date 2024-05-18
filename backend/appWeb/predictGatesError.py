import numpy as np
import xgboost as xgb

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
    formated_name = machine_name.split(" ")[1].capitalize()

    file = 'backend/models_xgboost/xgboost_gate_model_' + formated_name + '.model'
    xgb_model = xgb.Booster()
    xgb_model.load_model(file)

    data_np = np.array(data)
    matrix_data = xgb.DMatrix(data_np)

    prediction = xgb_model.predict(matrix_data)

    return prediction
