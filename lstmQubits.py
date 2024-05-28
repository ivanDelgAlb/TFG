import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import LSTM, Dense
from keras.models import load_model
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
import pytz
import matplotlib.dates as mdates

def preprocess_data(file_path, window_size):
    # Cargar el DataFrame
    df = pd.read_csv(file_path)

    # Cambiar el nombre de las columnas
    df = df.rename(columns={'y': 'T1', 'ds': 'date'})

    # Convertir la columna de fecha a tipo datetime y ordenar por fecha
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    # Normalizar datos (excepto la columna de fecha)
    fechas = df['date']
    df_sin_fechas = df.drop(columns=['date'])
    scaler = MinMaxScaler()
    df_normalizado = df_sin_fechas.apply(lambda fila: (fila - fila.min()) / (fila.max() - fila.min()), axis=1)
    df_normalizado['date'] = fechas

    print(df_normalizado)

    # Crear secuencias para entrenamiento y prueba
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
    # Obtener el índice del DataFrame correspondiente a la fecha proporcionada
    index_of_date = df.index[df['date'] == date].tolist()

    # Si la fecha no está presente, se crea una secuencia basada en los últimos datos disponibles en el DataFrame
    if not index_of_date:
        # Obtener la secuencia de los últimos "window_size" datos disponibles en el DataFrame
        sequence = df_normalized.iloc[-window_size:, :].values
    else:
        # Si la fecha está presente, obtener la secuencia de datos para la ventana de tiempo especificada
        index_of_date = index_of_date[0]  # Usar el primer índice si hay duplicados
        start_index = max(0, index_of_date - window_size + 1)  # Asegurar que el índice de inicio no sea negativo
        sequence = df_normalized.iloc[start_index:index_of_date + 1, :].values

    return sequence

def predict_future(model_path, data_file, window_size, future_date):
    # Cargar el modelo entrenado
    model = load_model(model_path)

    # Cargar el DataFrame y normalizar los datos
    df = pd.read_csv(data_file)

    # Cambiar el nombre de las columnas
    df = df.rename(columns={'y': 'T1', 'ds': 'date'})

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    df_sin_fechas = df.drop(columns=['date'])
    scaler = MinMaxScaler()
    df_normalizado = pd.DataFrame(scaler.fit_transform(df_sin_fechas), columns=df_sin_fechas.columns)

    # Obtener el punto de datos más reciente en el conjunto de datos
    current_date = datetime.now()

    # Convertir la fecha futura a un objeto datetime
    future_date = pd.to_datetime(future_date)

    # Calcular el número de pasos de tiempo entre el último punto de datos y la fecha futura
    num_steps = int((future_date - current_date).total_seconds() / (2 * 3600))  # Suponiendo intervalos de 2 horas

    # Generar las predicciones paso a paso
    current_input_sequence = get_sequence_for_date(df, df_normalizado, current_date, window_size)
    predictions = []
    for _ in range(num_steps):
        # Hacer la predicción para el siguiente paso de tiempo
        prediction = model.predict(np.expand_dims(current_input_sequence, axis=0))
        print(prediction)
        predictions.append(prediction)

        # Actualizar la secuencia de entrada con la predicción más reciente
        current_input_sequence = np.concatenate([current_input_sequence[1:], prediction], axis=0)

    # Convertir las predicciones en un arreglo numpy
    if len(predictions) == 0:
        raise ValueError("No predictions were generated.")
    predictions = np.array(predictions)

    # Aplanar el arreglo predictions
    predictions_flat = predictions.reshape(-1, predictions.shape[-1])

    # Invertir la normalización de las predicciones aplanadas
    predictions_inverted = scaler.inverse_transform(predictions_flat)

    # Reestructurar las predicciones invertidas a su forma original
    predictions_reshaped = predictions_inverted.reshape(predictions.shape)

    # Obtener solo los valores de error de puerta de las predicciones invertidas
    qubits_errors_predictions = predictions_reshaped[:, :, :5]

    return qubits_errors_predictions

def plot_predictions(predictions, future_date):
    current_date = datetime.now()
    future_date = pd.to_datetime(future_date)
    x_dates = pd.date_range(start=current_date, end=future_date, freq='2h')

    # Crear la figura y los ejes para gate_error_1
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Graficar las predicciones para gate_error_1
    ax1.plot(x_dates[:-1], predictions[:, :, 0].flatten(), label='T1', color='blue')

    # Formatear las fechas en el eje x
    date_format = mdates.DateFormatter('%d-%m-%y %H:%M:%S')
    ax1.xaxis.set_major_formatter(date_format)

    # Configurar el título y las etiquetas de los ejes para gate_error_1
    ax1.set_title('Predicción de T1')
    ax1.set_xlabel('Fecha y Hora')
    ax1.set_ylabel('Valor de predicción')

    # Rotar las fechas para una mejor visualización
    plt.xticks(rotation=45)

    # Agregar la leyenda
    ax1.legend()

    # Mostrar la primera gráfica
    plt.show()

    # Crear la figura y los ejes para gate_error_2
    fig, ax2 = plt.subplots(figsize=(10, 6))

    # Graficar las predicciones para gate_error_2
    ax2.plot(x_dates[:-1], predictions[:, :, 1].flatten(), label='T2', color='red')

    # Formatear las fechas en el eje x
    ax2.xaxis.set_major_formatter(date_format)

    # Configurar el título y las etiquetas de los ejes para gate_error_2
    ax2.set_title('Predicción de T2')
    ax2.set_xlabel('Fecha y Hora')
    ax2.set_ylabel('Valor de predicción')

    # Rotar las fechas para una mejor visualización
    plt.xticks(rotation=45)

    # Agregar la leyenda
    ax2.legend()

    # Mostrar la segunda gráfica
    plt.show()

machines = ["Brisbane", "Kyoto", "Osaka"]
window_size = 10
future_date = '2024-05-30' 

for machine in machines:
    print(machine)
    data_file = "backend/dataframes_neuralProphet/dataframeT1" + machine + ".csv"
    model_path = "backend/models_lstm_qubits/model_" + machine + ".keras"

    # Preprocesar datos
    X, y, scaler = preprocess_data(data_file, window_size)

    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Crear y entrenar
    create_model(X_train, y_train, X_test, y_test, model_path)
