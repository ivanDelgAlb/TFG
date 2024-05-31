import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import joblib

def create_model(machine_name, depth):
    """
    Creates and trains an xgBoost model from an existing dataframe.

    :param machine_name: The name of the quantum machine
    :type machine_name: str
    :param depth: The depth value to filter the dataset
    :type depth: int
    :return: None
    """
    formated_name = machine_name.split("_")[1].capitalize()
    
    columns = ['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_qubit_error',
               'n_qubits', 'depth', 't_gates', 'phase_gates', 'h_gates', 'cnot_gates', 'jensen-error']

    dataset = pd.read_csv(f'dataframes_perceptron/dataframe_perceptron_qubits_{formated_name}.csv')
    
    # Verificar si el dataset se cargó correctamente
    if dataset.empty:
        print(f"Dataset is empty for machine {machine_name} and depth {depth}")
        return
    
    dataset = dataset[(dataset['depth'] == depth) & (dataset['jensen-error'].notna())]
    dataset = dataset.drop(columns=['date'])
    
    # Verificar si el dataset tiene datos después de aplicar los filtros
    if dataset.empty:
        print(f"No data available after filtering for machine {machine_name} and depth {depth}")
        return

    # Convert columns to numeric
    for column in columns:
        dataset[column] = pd.to_numeric(dataset[column], errors='coerce')

    # Verificar si el dataset tiene datos después de eliminar filas con NaN
    if dataset.empty:
        print(f"No data available after dropping NaNs for machine {machine_name} and depth {depth}")
        return

    # Separate features and target
    target_column = 'jensen-error'
    feature_columns = ['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_qubit_error']
    additional_columns = ['n_qubits', 't_gates', 'phase_gates', 'h_gates', 'cnot_gates']

    X = dataset[feature_columns]
    y = dataset[target_column]
    additional_data = dataset[additional_columns]

    # Manual normalization
    X_normalized = X.apply(lambda fila: (fila - fila.min()) / (fila.max() - fila.min()), axis=1)
    X_normalized[additional_columns] = additional_data

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)

    params = {
        "objective": "reg:squarederror",
        "eval_metric": "rmse"
    }

    param_grid = {
        'max_depth': [3, 4, 5, 6],
        'learning_rate': [0.01, 0.05, 0.1],
        'n_estimators': [100, 200, 300],
        'colsample_bytree': [0.7, 0.8, 0.9, 1.0],
        'subsample': [0.7, 0.8, 0.9, 1.0]
    }

    xgb_model = xgb.XGBRegressor(**params)
    grid_search = GridSearchCV(estimator=xgb_model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error', verbose=1)
    grid_search.fit(X_train, y_train)

    best_params = grid_search.best_params_
    print("Best parameters found: ", best_params)

    final_model = xgb.XGBRegressor(**best_params)
    final_model.fit(X_train, y_train)

    predictions = final_model.predict(X_test)
    rmse = mean_squared_error(y_test, predictions, squared=False)
    print("RMSE:", rmse)

    # Save the model using joblib
    model_path = f'backend/models_xgboost_qubits/xgboost_qubit_model_{formated_name}_{depth}.joblib'
    joblib.dump(final_model, model_path)
    print("Model saved at:", model_path)
    
    # Optionally, plot predictions vs actual values
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, predictions, color='blue', label='Actual vs Predicted')
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
    plt.xlabel('Actual values')
    plt.ylabel('Predicted values')
    plt.title('Actual vs Predicted values')
    plt.legend()
    plt.show()
    


def predict(machine_name, data):
    """
    Predicts for the selected machine the error associated to the provided data
    :param machine_name: The name of the quantum machine
    :param data: The inputs for the model
    :type machine_name: String
    :type data: list of lists
    :return: The predicted value
    :rtype: list(float)
    """
    formated_name = machine_name.split("_")[1].capitalize()

    file = 'backend/models_xgboost_qubits/xgboost_gate_model_' + formated_name + "_" + depth + '.model'
    xgb_model = xgb.Booster()
    xgb_model.load_model(file)

    if data_np.ndim == 1:
        data_np = data_np.reshape(1, -1)

    matrix_data = xgb.DMatrix(data_np)

    prediction = xgb_model.predict(matrix_data)

    return prediction


machines = [ 'ibm_brisbane', 'ibm_kyoto', 'ibm_osaka']
depths = [5, 10, 15]

for machine in machines:
    for depth in depths:
        create_model(machine, depth)

        data = [0.001, 0.002, 5, 3, 1, 2, 4, 0.01, 0.02]  # Ejemplo de datos de entrada
        #prediction = predict(machine, data)
        #print(prediction)
