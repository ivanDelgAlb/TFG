import pandas as pd
from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.layers import Dense
from keras.models import load_model


def create_model(machine, X_train, X_test, y_train, y_test):
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='linear'))

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

    mse, mae = model.evaluate(X_test, y_test)
    print(f"MSE ({machine}):", mse)
    print(f"MAE ({machine}):", mae)

    directory = 'backend/models_perceptron/model_gates_' + machine + '.h5'
    model.save(directory)


def predict(machine, X_test, y_test):
    directory = 'backend/models_perceptron/model_gates_' + machine + '.h5'
    model = load_model(directory)
    reconstructed_data_X = model.predict(X_test)

    for i in range(len(X_test)):
        original_data_y = y_test.iloc[i]
        reconstructed_sample_X = reconstructed_data_X[i]
        print("Original_Y:", original_data_y)
        print("Reconstructed_X:", reconstructed_sample_X)
        print("\n")


machines = ["Brisbane", "Kyoto", "Osaka"]
for machine in machines:
    directory = 'backend/dataframes_perceptron/dataframe_perceptron_gates_' + machine + ".csv"
    dataFrame = pd.read_csv(directory)

    filtered_rows = dataFrame[(dataFrame['jensen-error'].notna())]
    filtered_rows = filtered_rows.apply(pd.to_numeric, errors='coerce')

    X = filtered_rows.drop(['date', 'kullback_error', 'jensen-error'], axis=1)

    print(X)
    y = filtered_rows['jensen-error'].loc[X.index]

    print(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    create_model(machine, X_train, X_test, y_train, y_test)

    #predict(machine, X_test, y_test)

print("Models created")

#predict()
