import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import xgboost as xgb

def create_model_qubits(machine_name):
    """
    Creates a xgBoost model from an existing dataframe
    :param machine_name: The name of the quantum machine
    :type machine_name: String
    :return: None
    """
    formated_name = machine_name.split("_")[1].capitalize() 

    columns = ['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_qubit_error', 'n_qubits', 'depth', 't_gates', 'phase_gates', 'h_gates', 'cnot_gates', 'jensen-error']

    dataset = pd.read_csv('scripts/experimentos/exp1/dataframe_experiment_qubit_' + formated_name + '.csv', names=columns)
    dataset = dataset[columns]

    for column in columns:
        dataset[column] = pd.to_numeric(dataset[column], errors='coerce')

    dataset = dataset.replace([np.inf, -np.inf], np.nan).dropna()

    target_column = 'jensen-error'

    x = dataset.drop(target_column, axis=1)
    y = dataset[target_column]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

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
    grid_search.fit(x_train_scaled, y_train)

    best_params = grid_search.best_params_
    print("Best parameters found: ", best_params)

    final_model = xgb.XGBRegressor(**best_params)
    final_model.fit(x_train_scaled, y_train)

    predictions = final_model.predict(x_test_scaled)
    rmse = mean_squared_error(y_test, predictions, squared=False)
    print("RMSE:", rmse)

    file = f'scripts/experimentos/experiment_xgboost_qubits_{formated_name}.json'
    final_model.save_model(file)
    print("Model created")


create_model_qubits("ibm_brisbane")
create_model_qubits("ibm_osaka")
create_model_qubits("ibm_kyoto")