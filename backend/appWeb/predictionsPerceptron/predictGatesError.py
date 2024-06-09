from datetime import datetime, timedelta
from keras.models import load_model
import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv()

def predict_gates_error(machine_name, predictions):
    try:
        machine_name = machine_name.split(" ")[1].capitalize()

        if os.getenv("DEPLOYMENT") == 'localhost': models_directory = os.path.join(os.getenv("PATH_FILE"), 'models_perceptron/')
        else: models_directory = os.path.join(os.environ['PWD'], 'models_perceptron/')

        model = load_model(models_directory + 'model_gates_' + machine_name + '.h5') 
        normalized_data = pd.DataFrame(predictions)
        errors = model.predict(normalized_data)
        errors = add_date_and_calibration(errors, predictions)
        return errors
    except FileNotFoundError:
        raise FileNotFoundError("The model is missing")

def add_date_and_calibration(errors, predictions):

    data_list = []
    date = datetime.now()

    for i, error in enumerate(errors):
        error_dict = {"Date": date.strftime("%Y-%m-%d %H:%M:%S")}
        date = date + timedelta(hours=2)
        error_dict['divergence'] = error[0]

        columns = ['error_gate_1_qubit', 'error_gate_2_qubit']

        if i < len(predictions):
            
            prediction = predictions[i]

            data = {
                'error_gate_1_qubit': prediction.get('error_gate_1_qubit', None),
                'error_gate_2_qubit': prediction.get('error_gate_2_qubit', None)
            }

            df = pd.DataFrame([data], columns=columns)
            
            df_inverted = pd.DataFrame(df, columns=['error_gate_1_qubit', 'error_gate_2_qubit'])
            
            error_dict['error_gate_1_qubit'] = df_inverted.iloc[0]['error_gate_1_qubit']
            error_dict['error_gate_2_qubit'] = df_inverted.iloc[0]['error_gate_2_qubit']
            
            data_list.append(error_dict)

    return data_list