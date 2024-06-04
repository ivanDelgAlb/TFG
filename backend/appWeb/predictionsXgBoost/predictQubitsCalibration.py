from keras.models import load_model
import pandas as pd
import numpy as np
from datetime import datetime
import joblib

def get_sequence_for_date(df, df_normalized, date, window_size):
    index_of_date = df.index[df['date'] == date].tolist()
    
    if not index_of_date:

        sequence = df_normalized.iloc[-window_size:, :].values
    else:
        index_of_date = index_of_date[0] 
        start_index = max(0, index_of_date - window_size + 1) 
        sequence = df_normalized.iloc[start_index:index_of_date + 1, :].values

    return sequence


def predict_future(machine, n_steps):
    machine_name = machine.split(" ")[1].capitalize()
    window_size = 10
    models_directory = "backend/models_lstm_qubits/"
    data_directory = "backend/dataframes_neuralProphet/"
    
    model = load_model(models_directory + "model_" + machine_name + ".keras")

    df = pd.read_csv(data_directory + "dataframeT1" + machine_name + ".csv")

    df = df.rename(columns={'ds': 'date'})

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    df_sin_fechas = df.drop(columns=['date'])
    columns = ['y', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error']
    df_numeric = pd.DataFrame(df_sin_fechas, columns=columns)
    scaler = joblib.load(f"{data_directory}scalerT1{machine_name}.pkl")
    df_normalizado = pd.DataFrame(scaler.transform(df_numeric), columns=df_sin_fechas.columns)
    df_normalizado = df_normalizado.rename(columns={'y': 'T1'})
    
    current_date = datetime.now()

    current_input_sequence = get_sequence_for_date(df, df_normalizado, current_date, window_size)
    predictions = []
    for _ in range(n_steps):
        
        prediction = model.predict(np.expand_dims(current_input_sequence, axis=0))
        predictions.append(prediction)

        current_input_sequence = np.concatenate([current_input_sequence[1:], prediction], axis=0)

    if len(predictions) == 0:
        raise ValueError("No predictions were generated.")
    predictions = np.array(predictions)

    predictions_flat = predictions.reshape(-1, predictions.shape[-1])
    df = pd.DataFrame(predictions_flat, columns=['y', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error'])

    predictions_inverted = scaler.inverse_transform(df)
    print(predictions_inverted)
    
    predictions_reshaped = predictions_inverted.reshape(predictions.shape)

    qubits_errors_predictions = predictions_reshaped[:, :, :5]

    return qubits_errors_predictions