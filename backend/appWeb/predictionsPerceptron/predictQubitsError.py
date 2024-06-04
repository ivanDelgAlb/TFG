from datetime import datetime, timedelta
from keras.models import load_model
import pandas as pd
import joblib

def predict_qubits_error(predictions, machine_name):
    try:
        machine_name = machine_name.split(" ")[1].capitalize()
        model = load_model('backend/models_perceptron/model_qubits_' + machine_name + '.h5') 
        normalized_data = pd.DataFrame(predictions)
        errors = model.predict(normalized_data)
        errors = add_date_and_calibration(errors, predictions, machine_name)
        return errors
    except FileNotFoundError:
        raise FileNotFoundError("The model is missing")
    
def add_date_and_calibration(errors, predictions, machine_name):
    data_list = []
    scaler_path = f'backend/dataframes_neuralProphet/scalerT1{machine_name}.pkl'

    scaler = joblib.load(scaler_path)
    date = datetime.now()

    for i, error in enumerate(errors):
        error_dict = {"Date": date.strftime("%Y-%m-%d %H:%M:%S")}
        date = date + timedelta(hours=2)
        error_dict['divergence'] = error[0]

        columns = ['y', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error']

        if i < len(predictions):
            
            prediction = predictions[i]
            data = {
                'y': prediction.get('T1', None),
                'T2': prediction.get('T2', None),
                'probMeas0Prep1': prediction.get('Prob0', None),
                'probMeas1Prep0': prediction.get('Prob1', None),
                'readout_error': prediction.get('Error', None)
            }

            df = pd.DataFrame([data], columns=columns)
            
            inverted_data = scaler.inverse_transform(df.values)
            df_inverted = pd.DataFrame(inverted_data, columns=['T1', 'T2', 'prob0', 'prob1', 'error'])

            error_dict['T1'] = df_inverted.iloc[0]['T1']
            error_dict['T2'] = df_inverted.iloc[0]['T2']
            error_dict['Prob0'] = df_inverted.iloc[0]['prob0']
            error_dict['Prob1'] = df_inverted.iloc[0]['prob1']
            error_dict['Error'] = df_inverted.iloc[0]['error']

        data_list.append(error_dict)

    return data_list


def normalized(predictions):
    print(predictions)

    df = pd.DataFrame(predictions)

    X = df.drop(['nQubits', 'tGates', 'phaseGates', 'hGates', 'cnotGates', 'depth'], axis=1)

    df_normalizado = X.apply(lambda fila: (fila - fila.min()) / (fila.max() - fila.min()), axis=1)

    df_normalizado['nQubits'] = df['nQubits']
    df_normalizado['tGates'] = df['tGates']
    df_normalizado['phaseGates'] = df['phaseGates']
    df_normalizado['hGates'] = df['hGates']
    df_normalizado['cnotGates'] = df['cnotGates']
    df_normalizado['depth'] = df['depth']

    return df_normalizado
