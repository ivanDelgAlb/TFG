from datetime import datetime, timedelta
from keras.models import load_model
import pandas as pd
import joblib
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def predict_qubits_error(predictions, machine_name, type):
    try:
        machine_name = machine_name.split(" ")[1].capitalize()

        if os.getenv("DEPLOYMENT") == 'localhost': models_directory = os.path.join(os.getenv("PATH_FILE"), 'models_neuralProphet/')
        else: models_directory = os.path.join(os.environ['PWD'], 'models_neuralProphet/')

        model = load_model(models_directory + 'model_qubits_' + machine_name + '.h5') 
        normalized_data = pd.DataFrame(predictions)
        print(normalized_data)
        if type == 'calibration': 
            columns_to_normalize = ["T1", "T2", "Prob0", "Prob1", "Error"]

            # Crear un DataFrame separado para las columnas normalizadas
            normalized_df = normalized_data[columns_to_normalize].apply(lambda row: (row - row.min()) / (row.max() - row.min()), axis=1)

            # Añadir las columnas normalizadas al DataFrame original
            normalized_data[["T1", "T2", "Prob0", "Prob1", "Error"]] = normalized_df
        errors = model.predict(normalized_data)
        errors = add_date_and_calibration(errors, predictions, machine_name, type)
        return errors
    except FileNotFoundError:
        raise FileNotFoundError("The model is missing")
    
def add_date_and_calibration(errors, predictions, machine_name, type):
    data_list = []

    if os.getenv("DEPLOYMENT") == 'localhost': scaler_path = os.path.join(os.getenv("PATH_FILE"), 'dataframes_neuralProphet/')
    else: scaler_path = os.path.join(os.environ['PWD'], 'dataframes_neuralProphet/')
    scaler_path = scaler_path + 'scalerT1' + machine_name + '.pkl'

    scaler = joblib.load(scaler_path)
    date = datetime.now()

    for i, error in enumerate(errors):
        error_dict = {"Date": date.strftime("%Y-%m-%d %H:%M:%S")}
        date = date + timedelta(hours=2)
        error_dict['divergence'] = error[0]

        columns = ['y', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error']

        if i < len(predictions):
            print(predictions)
            prediction = predictions[i]
            data = {
                'y': prediction.get('T1', None),
                'T2': prediction.get('T2', None),
                'probMeas0Prep1': prediction.get('Prob0', None),
                'probMeas1Prep0': prediction.get('Prob1', None),
                'readout_error': prediction.get('Error', None)
            }

            df = pd.DataFrame([data], columns=columns)
            
            if type == 'error':
                inverted_data = scaler.inverse_transform(df.values)
                df_inverted = pd.DataFrame(inverted_data, columns=['T1', 'T2', 'prob0', 'prob1', 'error'])
                
                error_dict['T1'] = df_inverted.iloc[0]['T1']
                error_dict['T2'] = df_inverted.iloc[0]['T2']
                error_dict['Prob0'] = df_inverted.iloc[0]['prob0']
                error_dict['Prob1'] = df_inverted.iloc[0]['prob1']
                error_dict['Error'] = df_inverted.iloc[0]['error']
            else:
                error_dict['T1'] = data['y']
                error_dict['T2'] = data['T2']
                error_dict['Prob0'] = data['probMeas0Prep1']
                error_dict['Prob1'] = data['probMeas1Prep0']
                error_dict['Error'] = data['readout_error']
            
            data_list.append(error_dict)

    return data_list
