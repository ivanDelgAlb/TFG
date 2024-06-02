import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error


def create_model_qubits(machine_name):
    """
    Creates a xgBoost model from an existing dataframe
    :param machine_name: The name of the quantum machine
    :type machine_name: String
    :return: None
    """
    formated_name = machine_name.split("_")[1].capitalize()

    columns = ['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_qubit_error', 'n_qubits', 'depth', 't_gates', 'phase_gates', 'h_gates', 'cnot_gates', 'jensen-error']

    dataset = pd.read_csv('backend/dataframes_perceptron/dataframe_perceptron_qubits_' + formated_name + '.csv', names=columns)
    dataset = dataset[columns]
    for column in columns:
        dataset[column] = pd.to_numeric(dataset[column], errors='coerce')

    dataset = dataset.replace([np.inf, -np.inf], np.nan)
    dataset = dataset.dropna()

    target_column = 'jensen-error'

    train_set, test_set = train_test_split(dataset, test_size=0.2)
    train_set = train_set.dropna(subset=[target_column])

    x_train = train_set.drop(target_column, axis=1)
    y_train = train_set[target_column]
    x_test = test_set.drop(target_column, axis=1)
    y_test = test_set[target_column]

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
    grid_search.fit(x_train, y_train)

    best_params = grid_search.best_params_
    print("Best parameters found: ", best_params)

    final_model = xgb.XGBRegressor(**best_params)
    final_model.fit(x_train, y_train)

    predictions = final_model.predict(x_test)

    rmse = mean_squared_error(y_test, predictions, squared=False)
    print("RMSE:", rmse)

    file = f'backend/models_xgboost/xgboost_qubit_model_{formated_name}.model'
    final_model.save_model(file)
    print("Model created")

    '''
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, predictions, color='blue', label='Datos reales vs Predicciones')
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
    plt.xlabel('Datos reales')
    plt.ylabel('Predicciones')
    plt.title('Predicciones vs Datos reales')
    plt.legend()
    plt.show()
    '''


def create_model_gates(machine_name):
    """
    Creates a xgBoost model from an existing dataframe
    :param machine_name: The name of the quantum machine
    :type machine_name: String
    :return: None
    """
    formated_name = machine_name.split("_")[1].capitalize()

    columns = ['gate_error_one_qubit', 'gate_error_two_qubit', 'n_qubits', 't_gates', 'phase_gates', 'h_gates', 'cnot_gates', 'jensen-error']

    dataset = pd.read_csv('dataframes_xgboost/dataframe_perceptron_gates_' + formated_name + '.csv', names=columns)
    dataset = dataset[columns]

    for column in columns:
        dataset[column] = pd.to_numeric(dataset[column], errors='coerce')

    dataset = dataset.replace([np.inf, -np.inf], np.nan)
    dataset = dataset.dropna()
    
    target_column = 'jensen-error'

    train_set, test_set = train_test_split(dataset, test_size=0.2)
    train_set = train_set.dropna(subset=[target_column])

    x_train = train_set.drop(target_column, axis=1)
    y_train = train_set[target_column]
    x_test = test_set.drop(target_column, axis=1)
    y_test = test_set[target_column]

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
    grid_search.fit(x_train, y_train)

    best_params = grid_search.best_params_
    print("Best parameters found: ", best_params)

    final_model = xgb.XGBRegressor(**best_params)
    final_model.fit(x_train, y_train)

    predictions = final_model.predict(x_test)

    rmse = mean_squared_error(y_test, predictions, squared=False)
    print("RMSE:", rmse)

    file = f'backend/models_xgboost/xgboost_gate_model_{formated_name}.model'
    final_model.save_model(file)
    print("Model created")

    '''
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, predictions, color='blue', label='Datos reales vs Predicciones')
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
    plt.xlabel('Datos reales')
    plt.ylabel('Predicciones')
    plt.title('Predicciones vs Datos reales')
    plt.legend()
    plt.show()
    '''


def predict_qubit(machine_name, data):
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

    file = 'backend/models_xgboost/xgboost_qubit_model_' + formated_name + '.model'
    xgb_model = xgb.Booster()
    xgb_model.load_model(file)

    data_np = np.array(data)

    if data_np.ndim == 1:
        data_np = data_np.reshape(1, -1)

    matrix_data = xgb.DMatrix(data_np)

    prediction = xgb_model.predict(matrix_data)

    return prediction.tolist()

def predict_gate(machine_name, data):
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

    file = 'backend/models_xgboost/xgboost_gate_model_' + formated_name + '.model'
    xgb_model = xgb.Booster()
    xgb_model.load_model(file)

    data_np = np.array(data)

    if data_np.ndim == 1:
        data_np = data_np.reshape(1, -1)

    matrix_data = xgb.DMatrix(data_np)

    prediction = xgb_model.predict(matrix_data)

    return prediction


create_model_qubits("ibm_brisbane")
create_model_qubits("ibm_osaka")
create_model_qubits("ibm_kyoto")

'''
machine_name = "ibm_brisbane"
data = [165.4125864953162,138.33769254466574,0.0145999999999999,0.0082,0.0113999999999999,15,15,12.0,13.0,13.0,61.0]
prediction = predict_qubit(machine_name, data)
print(prediction)
'''
'''
machine_name = "ibm_brisbane"
data = [
    [0.001, 0.002, 5, 3, 1, 2, 4, 0.01, 0.02],
    [0.003, 0.001, 10, 5, 2, 3, 6, 0.015, 0.025]
]
predictions = predict(machine_name, data)
print(predictions)
'''