import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import LSTM, Dense
from keras.models import load_model
import matplotlib.pyplot as plt
from datetime import datetime



def preprocess_data(file_path, window_size):
    df = pd.read_csv(file_path)

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    def create_sequences(data, window_size):
        X, y = [], []
        for i in range(len(data) - window_size):
            X.append(data[i:i + window_size])
            y.append(data[i + window_size])
        return np.array(X), np.array(y)

    X, y = create_sequences(df[['gate_error_1', 'gate_error_2']].values, window_size)

    return X, y



def create_model(X_train, y_train, X_test, y_test, model_path):
    model = Sequential([
        LSTM(100, input_shape=(X_train.shape[1], X_train.shape[2])),
        Dense(2)
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


def predict_future(model_path, data_file, window_size, future_date):
    model = load_model(model_path)

    df = pd.read_csv(data_file)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    df_sin_fechas = df.drop(columns=['date'])
    df_normalizado = pd.DataFrame(df_sin_fechas, columns=df_sin_fechas.columns)

    current_date = datetime.now()

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

    gate_errors_predictions = predictions_flat[:, :, :2]

    return gate_errors_predictions


machines = ["Brisbane", "Kyoto", "Osaka"]
window_size = 10
future_date = '2024-05-24'

for machine in machines:

    data_file = f"backend/dataframes_gates/dataframe_Gates{machine}.csv"
    model_path = f"backend/models_lstm/model_{machine}.keras"

    X, y = preprocess_data(data_file, window_size)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    create_model(X_train, y_train, X_test, y_test, model_path)

