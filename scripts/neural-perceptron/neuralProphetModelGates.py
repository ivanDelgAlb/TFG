from neuralprophet import NeuralProphet, set_log_level
import pandas as pd
import pickle


def create_model_gates(file):
    """
    Creates a NeuralProphet model in the directory models_neuralProphet from the given dataframe
    :param file: A csv dataframe of the data
    :return: None
    """

    directory = '../../backend/dataframes_neuralProphet/'
    df = pd.read_csv(directory + file, encoding="latin1")
    columns = df.columns.to_list()

    start = file.find("dataframe") + len("dataframe")
    end = file.find(".csv")
    substring = file[start:end]

    train_index = int(len(df) * 0.8)
    df_train = df.iloc[:train_index]
    df_test = df.iloc[train_index:]

    model = NeuralProphet(
        n_forecasts=1,
        learning_rate=0.1
    )

    set_log_level("ERROR")

    model.add_lagged_regressor(columns[2])

    model.set_plotting_backend("plotly-static")

    metrics = model.fit(df=df_train, freq="2H", validation_df=df_test)
    print(metrics)

    file_name = '../../backend/models_neuralProphet/model' + substring + '.pkl'
    with open(file_name, "wb") as file:
        pickle.dump(model, file)


def predict_qubits(n_steps, machine_name):
    """
    Predicts the configuration for a given machine in n_steps (each step is an hour)
    :param n_steps: the number of steps to predict
    :param machine_name: the name of the machine to predict the configuration
    :return: A dataframe with the past data and the predicted ones
    :rtype: pandas.core.frame.DataFrame
    """

    machine_name = machine_name.split("_")[1].capitalize()

    try:
        models_directory = '../../backend/models_neuralProphet/'
        with open(models_directory + 'modelError1' + machine_name + '.pkl', "rb") as file:
            model_error_1 = pickle.load(file)
        with open(models_directory + 'modelError2' + machine_name + '.pkl', "rb") as file:
            model_error_2 = pickle.load(file)

        dataframes_directory = '../../backend/dataframes_neuralProphet/'

        df_error_1 = pd.read_csv(dataframes_directory + 'dataframeError1' + machine_name + '.csv', encoding="latin1")
        df_error_2 = pd.read_csv(dataframes_directory + 'dataframeError2' + machine_name + '.csv', encoding="latin1")

        model_error_1.restore_trainer()
        model_error_2.restore_trainer()

        future_error_1 = model_error_1.make_future_dataframe(df=df_error_1, n_historic_predictions=True, periods=n_steps)
        future_error_2 = model_error_2.make_future_dataframe(df=df_error_2, n_historic_predictions=True, periods=n_steps)

        for i in range(n_steps):

            forecast_future_error_1 = model_error_1.predict(future_error_1)
            forecast_future_error_2 = model_error_2.predict(future_error_2)

            future_error_1.iloc[-1, future_error_1.columns.get_loc('y')] = forecast_future_error_1[-1:]['yhat1']
            future_error_1.iloc[-1, future_error_1.columns.get_loc('error_2')] = forecast_future_error_2[-1:]['yhat1']

            future_error_2.iloc[-1, future_error_2.columns.get_loc('error_1')] = forecast_future_error_1[-1:]['yhat1']
            future_error_2.iloc[-1, future_error_2.columns.get_loc('y')] = forecast_future_error_2[-1:]['yhat1']

            if i != n_steps - 1:
                future_error_1 = model_error_1.make_future_dataframe(df=future_error_1, n_historic_predictions=True, periods=n_steps)
                future_error_2 = model_error_2.make_future_dataframe(df=future_error_2, n_historic_predictions=True, periods=n_steps)
        '''
        model_error_1.highlight_nth_step_ahead_of_each_forecast(1)
        model_error_1.plot(forecast_future_error_1[-12:])
        '''
        return future_error_1

    except FileNotFoundError:
        raise FileNotFoundError("One of the models is missing")

'''
machines = ["Brisbane", "Kyoto", "Osaka"]
files = ["dataframeError1", "dataframeError2"]

for machine in machines:
    for file in files:
        print("Maquina: " + machine + ", fichero: " + file)
        csv = file + machine + '.csv'
        create_model_gates(csv)
print("Models created")
'''

future_Error_1 = predict_qubits(1, "ibm_Brisbane")
print(future_Error_1)
