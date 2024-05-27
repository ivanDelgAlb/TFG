from keras.models import load_model
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from datetime import datetime
import pytz

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


def predict_future(machine, n_steps):
    machine_name = machine.split(" ")[1].capitalize()
    window_size = 10
    models_directory = "backend/models_lstm/"
    data_directory = "backend/dataframes_gates/"
    # Cargar el modelo entrenado
    model = load_model(models_directory + "model_" + machine_name + ".keras")

    # Cargar el DataFrame y normalizar los datos
    df = pd.read_csv(data_directory + "dataframe_Gates" + machine_name + ".csv")
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    df_sin_fechas = df.drop(columns=['date'])
    scaler = MinMaxScaler()
    df_normalizado = pd.DataFrame(scaler.fit_transform(df_sin_fechas), columns=df_sin_fechas.columns)

    # Obtener el punto de datos más reciente en el conjunto de datos
    current_date = datetime.now()

    

    # Convertir la fecha futura a un objeto datetime

    current_date_aware = current_date.replace(tzinfo=pytz.UTC)

    # Generar las predicciones paso a paso
    current_input_sequence = get_sequence_for_date(df, df_normalizado, current_date_aware, window_size)
    predictions = []
    for _ in range(n_steps):
        
        
        # Hacer la predicción para el siguiente paso de tiempo
        prediction = model.predict(np.expand_dims(current_input_sequence, axis=0))

        predictions.append(prediction)

        # Actualizar la secuencia de entrada con la predicción más reciente
        current_input_sequence = np.concatenate([current_input_sequence[1:], prediction], axis=0)

    # Convertir las predicciones en un arreglo numpy
    predictions = np.array(predictions)

    # Aplanar el arreglo predictions
    predictions_flat = predictions.reshape(-1, predictions.shape[-1])

    # Invertir la normalización de las predicciones aplanadas
    predictions_inverted = scaler.inverse_transform(predictions_flat)

    # Reestructurar las predicciones invertidas a su forma original
    predictions_reshaped = predictions_inverted.reshape(predictions.shape)

    # Obtener solo los valores de error de puerta de las predicciones invertidas
    gate_errors_predictions = predictions_reshaped[:, :, :2]

    return gate_errors_predictions