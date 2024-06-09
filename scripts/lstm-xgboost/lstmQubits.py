import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import LSTM, Dense
from keras.models import load_model
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
import matplotlib.dates as mdates
import joblib

def preprocess_data(scaler_path, file_path, window_size):
    df = pd.read_csv(file_path)

    df = df.rename(columns={'y': 'T1', 'ds': 'date'})

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    fechas = df['date']
    df_sin_fechas = df.drop(columns=['date'])
    scaler = joblib.load(scaler_path)
    df_normalizado = scaler.fit_transform(df_sin_fechas)

    df_normalizado = pd.DataFrame(df_normalizado, columns=df_sin_fechas.columns)
    df_normalizado['date'] = fechas

    (df_normalizado)

    def create_sequences(data, window_size):
        X, y = [], []
        for i in range(len(data) - window_size):
            X.append(data[i:i + window_size])
            y.append(data[i + window_size])
        return np.array(X), np.array(y)

    X, y = create_sequences(df_normalizado[['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error']].values, window_size)

    return X, y, scaler

def create_model(X_train, y_train, X_test, y_test, model_path):
    model = Sequential([
        LSTM(100, input_shape=(X_train.shape[1], X_train.shape[2])),
        Dense(5)  
    ])
    model.compile(loss='mse', optimizer='adam')
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))
    model.save(model_path)

def get_sequence_for_date(df, df_normalized, date, window_size):
    index_of_date = df.index[df['date'] == date].tolist()

    if not index_of_date:
        sequence = df_normalized.iloc[-window_size:, :].values
    else:
        index_of_date = index_of_date[0]
        start_index = max(0, index_of_date - window_size + 1)
        sequence = df_normalized.iloc[start_index:index_of_date + 1, :].values

    return sequence

def predict_future(scaler_path, model_path, data_file, window_size, future_date):
    model = load_model(model_path)

    df = pd.read_csv(data_file)

    df = df.rename(columns={'y': 'T1', 'ds': 'date'})

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    df_sin_fechas = df.drop(columns=['date'])
    scaler = joblib.load(scaler_path)
    df_normalizado = pd.DataFrame(scaler.fit_transform(df_sin_fechas), columns=df_sin_fechas.columns)

    current_date = datetime.now()

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

def plot_predictions(predictions, future_date):
    current_date = datetime.now()
    future_date = pd.to_datetime(future_date)
    x_dates = pd.date_range(start=current_date, end=future_date, freq='2h')

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.plot(x_dates[:-1], predictions[:, :, 0].flatten(), label='T1', color='blue')

    date_format = mdates.DateFormatter('%d-%m-%y %H:%M:%S')
    ax1.xaxis.set_major_formatter(date_format)

    ax1.set_title('Predicción de T1')
    ax1.set_xlabel('Fecha y Hora')
    ax1.set_ylabel('Valor de predicción')

    plt.xticks(rotation=45)

    ax1.legend()

    plt.show()

    fig, ax2 = plt.subplots(figsize=(10, 6))

    ax2.plot(x_dates[:-1], predictions[:, :, 1].flatten(), label='T2', color='red')

    ax2.xaxis.set_major_formatter(date_format)

    ax2.set_title('Predicción de T2')
    ax2.set_xlabel('Fecha y Hora')
    ax2.set_ylabel('Valor de predicción')

    plt.xticks(rotation=45)

    ax2.legend()

    plt.show()

machines = ["Brisbane", "Kyoto", "Osaka"]
window_size = 10
future_date = '2024-05-30' 

for machine in machines:
    (machine)
    data_file = "backend/dataframes_neuralProphet/dataframeT1" + machine + ".csv"
    model_path = "backend/models_lstm_qubits/model_" + machine + ".keras"
    scaler_path = 'backend/dataframes_neuralProphet/scalerT1' + machine + '.pkl'

    X, y, scaler = preprocess_data(scaler_path, data_file, window_size)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    create_model(X_train, y_train, X_test, y_test, model_path)
