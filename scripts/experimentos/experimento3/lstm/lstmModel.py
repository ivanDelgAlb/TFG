import pandas as pd
import numpy as np
from keras.models import load_model
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

def predict_future_qubits(scaler_path, model_path, data_file, window_size, future_date):
    model = load_model(model_path)

    df = pd.read_csv(data_file)

    df = df.rename(columns={'y': 'T1', 'ds': 'date'})

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    df_sin_fechas = df.drop(columns=['date'])
    scaler = joblib.load(scaler_path)
    df_normalizado = pd.DataFrame(scaler.fit_transform(df_sin_fechas), columns=df_sin_fechas.columns)

    current_date = pd.to_datetime('2024-06-03 11:50:00')

    future_date = pd.to_datetime(future_date)

    num_steps = int((future_date - current_date).total_seconds() / (2 * 3600))

    current_input_sequence = get_sequence_for_date(df, df_normalizado, current_date, window_size)
    predictions = []
    for _ in range(num_steps):
        prediction = model.predict(np.expand_dims(current_input_sequence, axis=0))
        (prediction)
        predictions.append(prediction)

        current_input_sequence = np.concatenate([current_input_sequence[1:], prediction], axis=0)

    if len(predictions) == 0:
        raise ValueError("No predictions were generated.")
    predictions = np.array(predictions)

    predictions_flat = predictions.reshape(-1, predictions.shape[-1])

    predictions_inverted = scaler.inverse_transform(predictions_flat)

    predictions_reshaped = predictions_inverted.reshape(predictions.shape)

    qubits_errors_predictions = predictions_reshaped[:, :, :5]

    return qubits_errors_predictions


def predict_future_gates(model_path, data_file, window_size, future_date):
    model = load_model(model_path)

    df = pd.read_csv(data_file)
    df = df.rename(columns={'ds': 'date'})
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    df_sin_fechas = df.drop(columns=['date'])
    df_normalizado = pd.DataFrame(df_sin_fechas, columns=df_sin_fechas.columns)

    current_date = pd.to_datetime('2024-06-03 11:50:00')

    future_date = pd.to_datetime(future_date)

    num_steps = int((future_date - current_date).total_seconds() / (2 * 3600))

    current_input_sequence = get_sequence_for_date(df, df_normalizado, current_date, window_size)
    predictions = []
    for _ in range(num_steps):
        prediction = model.predict(np.expand_dims(current_input_sequence, axis=0))
        predictions.append(prediction)
        current_input_sequence = np.concatenate([current_input_sequence[1:], prediction], axis=0)

    predictions = np.array(predictions)

    predictions_flat = predictions.reshape(-1, predictions.shape[-1])

    gate_errors_predictions = predictions[:, :, :2]

    return gate_errors_predictions


machines = ["Brisbane", "Kyoto", "Osaka"]
window_size = 10
future_date = '2024-06-07 10:00:00' 

for machine in machines:
    data_file = "backend/dataframes_neuralProphet/dataframeT1" + machine + ".csv"
    model_path = "backend/models_lstm_qubits/model_" + machine + ".keras"
    scaler_path = 'backend/dataframes_neuralProphet/scalerT1' + machine + '.pkl'
    scaler = joblib.load(scaler_path)

    predictions = predict_future_qubits(scaler_path, model_path, data_file, window_size, future_date)

    predictions = np.array(predictions)
    predictions = predictions.reshape(-1, 5)

    time = pd.date_range(start='2024-06-03 11:50:00', periods=len(predictions), freq='2H')

    predictions = scaler.inverse_transform(predictions)
    df = pd.DataFrame(predictions, columns=['T1', 'T2', 'Prob0', 'Prob1', 'Error'])
    df['Date'] = time

    df = df[['Date', 'T1', 'T2', 'Prob0', 'Prob1', 'Error']]

    df.to_csv('scripts/experimentos/experimento3/lstm/dataframe_experimentLSTMQubits' + machine + '.csv', index=False)

for machine in machines:
    data_file = "backend/dataframes_neuralProphet/dataframeError1" + machine + ".csv"
    model_path = "backend/models_lstm/model_" + machine + ".keras"

    predictions = predict_future_gates(model_path, data_file, window_size, future_date)

    predictions = np.array(predictions)
    predictions = predictions.reshape(-1, 2)

    time = pd.date_range(start='2024-06-03 11:50:00', periods=len(predictions), freq='2H')

    df = pd.DataFrame(predictions, columns=['Error1', 'Error2'])
    df['Date'] = time

    df = df[['Date', 'Error1', 'Error2']]

    df.to_csv('scripts/experimentos/experimento3/lstm/dataframe_experimentLSTMGates' + machine + '.csv', index=False)

