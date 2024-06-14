import pandas as pd
from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from keras.models import load_model


def create_model(machine, X_train, X_test, y_train, y_test):
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='linear'))

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

    mse, mae = model.evaluate(X_test, y_test)
    print(f"Error cuadrático medio ({machine}):", mse)
    print(f"Error absoluto medio ({machine}):", mae)

    directory = '../../backend/models_perceptron/model_qubits_' + machine +'.keras'
    model.save(directory)
    

def predict(machine, X_test, y_test):
    directory = '../../backend/models_perceptron/model_qubits_' + machine + '.h5'
    model = load_model(directory)
    reconstructed_data_X = model.predict(X_test)

    for i in range(len(X_test)):
        original_data_y = y_test.iloc[i]
        reconstructed_sample_X = reconstructed_data_X[i]
        print("Original_Y:", original_data_y)
        print("Reconstruido_X:", reconstructed_sample_X)
        print("\n")


machines = ["Brisbane", "Kyoto", "Osaka"]
for machine in machines:
    directory = '../../backend/dataframes_perceptron/dataframe_perceptron_qubits_' + machine + '.csv'
    dataFrame = pd.read_csv(directory)

    filas_filtradas = dataFrame[(dataFrame['jensen-error'].notna())]

    X = filas_filtradas.drop(['date', 'n_qubits', 'depth', 't_gates', 'phase_gates', 'h_gates', 'cnot_gates', 'kullback_error', 'jensen-error'], axis=1)

    X_normalizado = X.apply(lambda fila: (fila - fila.min()) / (fila.max() - fila.min()), axis=1)

    X_normalizado['n_qubits'] = filas_filtradas['n_qubits']
    X_normalizado['depth'] = filas_filtradas['depth']
    X_normalizado['t_gates'] = filas_filtradas['t_gates']
    X_normalizado['phase_gates'] = filas_filtradas['phase_gates']
    X_normalizado['h_gates'] = filas_filtradas['h_gates']
    X_normalizado['cnot_gates'] = filas_filtradas['cnot_gates']

    y = filas_filtradas['jensen-error']

    X_train, X_test, y_train, y_test = train_test_split(X_normalizado, y, test_size=0.2, random_state=42)

    create_model(machine, X_train, X_test, y_train, y_test)

    #predict(machine, X_test, y_test)

print("Models created")

#predict()

