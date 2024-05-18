import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
from keras.models import load_model

from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.optimizers import Adam

def createModel(maquina):
    # Definir y compilar el modelo LSTM
    model = Sequential([
        LSTM(100, input_shape=(X.shape[1], X.shape[2])),
        Dense(4)  # 2 salidas para las columnas gate_error_1 y gate_error_2
    ])

    model.compile(loss=MeanSquaredError(), optimizer=Adam())

    
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))
    directorio = 'models_lstm/'
    nombre_archivo = directorio + 'model_'+ maquina + '.h5'

    model.save(nombre_archivo)
    print("Modelo guardado con éxito")


def predict(maquina, fecha_prediccion):
    formatearNombre = maquina.split("_")[1].capitalize()
    directorio = 'models_lstm/'
    nombre_archivo = directorio + 'model_'+ formatearNombre + '.h5'
    model = load_model(nombre_archivo)

    df = pd.read_csv('dataframes_gates/dataframe_Gates' + formatearNombre + '.csv')

    df['date'] = pd.to_datetime(df['date'])

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df[['gate_error_1', 'gate_error_2', 'gate_length_1', 'gate_length_2']])

    def get_sequence_for_date(df, scaled_data, date, seq_length):
        data_up_to_date = df[df['date'] <= date]

        start_index = len(data_up_to_date) - seq_length
        sequence = scaled_data[start_index:start_index + seq_length, :]
        
        return sequence

    fecha_prediccion = pd.to_datetime(fecha_prediccion)

    seq_length = 10
    input_sequence = get_sequence_for_date(df, scaled_data, fecha_prediccion, seq_length)

    input_sequence = np.expand_dims(input_sequence, axis=0)

    prediccion = model.predict(input_sequence)

    prediccion_invertida = scaler.inverse_transform(
        np.hstack((prediccion, np.zeros((prediccion.shape[0], scaled_data.shape[1] - prediccion.shape[1]))))
    )
    result = prediccion[0, :2]
    return result[0], result[1]

    '''
    predictions = model.predict(X_test)

    # Graficar las predicciones y los valores reales
    plt.plot(predictions[:, 1], label='Predicción gate_error_2')
    plt.plot(y_test[:, 1], label='Valor Real gate_error_2')
    plt.legend()
    plt.show()

    plt.plot(predictions[:, 0], label='Predicción gate_error_1')
    plt.plot(y_test[:, 0], label='Valor Real gate_error_1')
    plt.legend()
    plt.show()
    '''

'''
maquinas = ["ibm_brisbane", "ibm_kyoto", "ibm_osaka"] 

for maquina in maquinas:
    # Cargar el DataFrame
    formatearNombre = maquina.split("_")[1].capitalize()
    directorio = 'dataframes_gates/'
    nombre_archivo = directorio + 'dataframe_Gates'+ formatearNombre + '.csv'
    df = pd.read_csv(nombre_archivo)

    # Convertir la columna de fecha a tipo datetime
    df['date'] = pd.to_datetime(df['date'])

    # Ordenar el DataFrame por fecha si no está ordenado
    df = df.sort_values(by='date')

    # Normalizar los datos (opcional pero recomendado)
    scaler = MinMaxScaler()
    df[['gate_error_1', 'gate_error_2', 'gate_length_1', 'gate_length_2']] = scaler.fit_transform(df[['gate_error_1', 'gate_error_2', 'gate_length_1', 'gate_length_2']])

    # Definir ventana de tiempo y función para crear secuencias
    window_size = 10

    def create_sequences(data, window_size):
        X, y = [], []
        for i in range(len(data) - window_size):
            X.append(data[i:i+window_size])
            y.append(data[i+window_size])
        return np.array(X), np.array(y)

    # Convertir los datos en secuencias
    X, y = create_sequences(df[['gate_error_1', 'gate_error_2','gate_length_1', 'gate_length_2']].values, window_size)

    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    createModel(formatearNombre)
'''
print(predict('ibm_Brisbane', '2024-04-09 17:00:00'))