import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras import Sequential
from keras.layers import LSTM, Dense
from keras.models import load_model
import matplotlib.pyplot as plt

def createModel():
    
    # Definir y compilar el modelo LSTM
    model = Sequential([
        LSTM(100, input_shape=(X.shape[1], X.shape[2])),
        Dense(4)  # 2 salidas para las columnas gate_error_1 y gate_error_2
    ])

    model.compile(loss='mse', optimizer='adam')

    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

    model.save("models_lstm/model_Brisbane.keras")

def predict():
    model = load_model('models_lstm/model_Brisbane.keras')
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

# Cargar el DataFrame
df = pd.read_csv("dataframes_gates/dataframe_GatesBrisbane.csv")

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

createModel()
predict()


