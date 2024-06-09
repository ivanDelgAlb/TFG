from keras.models import load_model
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from datetime import datetime
import pytz
import joblib

import os
from dotenv import load_dotenv

load_dotenv()


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

    if os.getenv("DEPLOYMENT") == 'localhost': models_directory = os.path.join(os.getenv("PATH_FILE"), 'models_lstm/')
    else: models_directory = os.path.join(os.environ['PWD'], 'models_lstm/')

    if os.getenv("DEPLOYMENT") == 'localhost': data_directory = os.path.join(os.getenv("PATH_FILE"), 'dataframes_gates/')
    else: data_directory = os.path.join(os.environ['PWD'], 'dataframes_gates/')

    model = load_model(models_directory + "model_" + machine_name + ".keras")

    df = pd.read_csv(data_directory + "dataframe_Gates" + machine_name + ".csv")
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    df_sin_fechas = df.drop(columns=['date'])

    current_date = datetime.now()

    current_date_aware = current_date.replace(tzinfo=pytz.UTC)

    current_input_sequence = get_sequence_for_date(df, df_sin_fechas, current_date_aware, window_size)
    predictions = []
    for _ in range(n_steps):
        
        prediction = model.predict(np.expand_dims(current_input_sequence, axis=0))

        predictions.append(prediction)

        current_input_sequence = np.concatenate([current_input_sequence[1:], prediction], axis=0)

    predictions = np.array(predictions)

    predictions_flat = predictions.reshape(-1, predictions.shape[-1])

    predictions_reshaped = predictions_flat.reshape(predictions.shape)

    gate_errors_predictions = predictions_reshaped[:, :, :2]

    return gate_errors_predictions