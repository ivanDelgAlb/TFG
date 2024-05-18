from keras.models import load_model
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def predict(maquina, fecha_prediccion_iso):
    formatearNombre = maquina.split(" ")[1].capitalize()
    directorio = 'models_lstm/'
    nombre_archivo = directorio + 'model_' + formatearNombre + '.h5'
    model = load_model(nombre_archivo)

    df = pd.read_csv('backend/dataframes_gates/dataframe_Gates' + formatearNombre + '.csv')
    
    # Convertir la columna de fecha y la fecha de predicción al mismo formato
    df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
    fecha_prediccion = pd.to_datetime(fecha_prediccion_iso).tz_localize(None)

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df[['gate_error_1', 'gate_error_2', 'gate_length_1', 'gate_length_2']])

    def get_sequence_for_date(df, scaled_data, date, seq_length):
        data_up_to_date = df[df['date'] <= date]

        if len(data_up_to_date) < seq_length:
            raise ValueError("No hay suficientes datos antes de la fecha dada para crear una secuencia.")
        
        start_index = len(data_up_to_date) - seq_length
        sequence = scaled_data[start_index:start_index + seq_length, :]
        
        return sequence

    seq_length = 10
    input_sequence = get_sequence_for_date(df, scaled_data, fecha_prediccion, seq_length)

    input_sequence = np.expand_dims(input_sequence, axis=0)

    prediccion = model.predict(input_sequence)

    prediccion_invertida = scaler.inverse_transform(
        np.hstack((prediccion, np.zeros((prediccion.shape[0], scaled_data.shape[1] - prediccion.shape[1]))))
    )
    
    result = prediccion_invertida[0, :2]
    return result[0], result[1]

