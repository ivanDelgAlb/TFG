from datetime import datetime, timedelta
from keras.models import load_model
import pandas as pd
import joblib


def predict_gates_error(predictions, machine_name):
    try:
        machine_name = machine_name.split(" ")[1].capitalize()
        model = load_model('backend/models_perceptron/model_gates_' + machine_name + '.h5') 
        normalized_data = pd.DataFrame(predictions)
        errors = model.predict(normalized_data)
        errors = add_date_and_calibration(errors, predictions, machine_name)
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

        columns = ['y', 'Error2']

        if i < len(predictions):
            
            prediction = predictions[i]
            data = {
                'y': prediction.get('Error1', None),
                'Error2': prediction.get('Error2', None)
            }

            df = pd.DataFrame([data], columns=columns)
            
            df_inverted = pd.DataFrame(df, columns=['Error_gate_1_qubit', 'Error_gate_2_qubit'])
            
            error_dict['T1'] = df_inverted.iloc[0]['T1']
            error_dict['T2'] = df_inverted.iloc[0]['T2']
            error_dict['Prob0'] = df_inverted.iloc[0]['prob0']
            error_dict['Prob1'] = df_inverted.iloc[0]['prob1']
            error_dict['Error'] = df_inverted.iloc[0]['error']

            
            data_list.append(error_dict)

    return data_list