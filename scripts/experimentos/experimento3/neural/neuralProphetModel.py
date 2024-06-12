import pandas as pd
import pickle
import joblib


def predict_gates(n_steps, machine_name):
    """
    Predicts the configuration for a given machine in n_steps (each step is an hour)
    :param n_steps: the number of steps to predict
    :param machine_name: the name of the machine to predict the configuration
    :return: A dataframe with the past data and the predicted ones
    :rtype: pandas.core.frame.DataFrame
    """

    try:
        models_directory = 'backend/models_neuralProphet/'
        with open(models_directory + 'modelError1' + machine_name + '.pkl', "rb") as file:
            model_error_1 = pickle.load(file)
        with open(models_directory + 'modelError2' + machine_name + '.pkl', "rb") as file:
            model_error_2 = pickle.load(file)

        dataframes_directory = 'backend/dataframes_neuralProphet/'

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

        return future_error_1

    except FileNotFoundError:
        raise FileNotFoundError("One of the models is missing")


def predict_qubits(n_steps, machine_name):
    """
    Predicts the configuration for a given machine in n_steps (each step is an hour)
    :param n_steps: the number of steps to predict
    :param machine_name: the name of the machine to predict the configuration
    :return: A dataframe with the past data and the predicted ones
    :rtype: pandas.core.frame.DataFrame
    """

    try:
        models_directory = 'backend/models_neuralProphet/'
        with open(models_directory + 'modelT1' + machine_name + '.pkl', "rb") as file:
            model_T1 = pickle.load(file)
        with open(models_directory + 'modelT2' + machine_name + '.pkl', "rb") as file:
            model_T2 = pickle.load(file)
        with open(models_directory + 'modelProb0' + machine_name + '.pkl', "rb") as file:
            model_Prob0 = pickle.load(file)
        with open(models_directory + 'modelProb1' + machine_name + '.pkl', "rb") as file:
            model_Prob1 = pickle.load(file)
        with open(models_directory + 'modelError' + machine_name + '.pkl', "rb") as file:
            model_error = pickle.load(file)
        
        dataframes_directory = 'backend/dataframes_neuralProphet/'

        df_T1 = pd.read_csv(dataframes_directory + 'dataframeT1' + machine_name + '.csv', encoding="latin1")
        df_T2 = pd.read_csv(dataframes_directory + 'dataframeT2' + machine_name + '.csv', encoding="latin1")
        df_Prob0 = pd.read_csv(dataframes_directory + 'dataframeProb0' + machine_name + '.csv', encoding="latin1")
        df_Prob1 = pd.read_csv(dataframes_directory + 'dataframeProb1' + machine_name + '.csv', encoding="latin1")
        df_error = pd.read_csv(dataframes_directory + 'dataframeError' + machine_name + '.csv', encoding='latin1')

        model_T1.restore_trainer()
        model_T2.restore_trainer()
        model_Prob0.restore_trainer()
        model_Prob1.restore_trainer()
        model_error.restore_trainer()

        future_T1 = model_T1.make_future_dataframe(df=df_T1, n_historic_predictions=True, periods=n_steps)
        future_T2 = model_T2.make_future_dataframe(df=df_T2, n_historic_predictions=True, periods=n_steps)
        future_Prob0 = model_Prob0.make_future_dataframe(df=df_Prob0, n_historic_predictions=True, periods=n_steps)
        future_Prob1 = model_Prob1.make_future_dataframe(df=df_Prob1, n_historic_predictions=True, periods=n_steps)
        future_error = model_error.make_future_dataframe(df=df_error, n_historic_predictions=True, periods=n_steps)

        for i in range(n_steps):

            forecast_future_T1 = model_T1.predict(future_T1)
            forecast_future_T2 = model_T2.predict(future_T2)
            forecast_future_Prob0 = model_Prob0.predict(future_Prob0)
            forecast_future_Prob1 = model_Prob1.predict(future_Prob1)
            forecast_future_error = model_error.predict(future_error)
            
            future_T1.iloc[-1, future_T1.columns.get_loc('y')] = forecast_future_T1[-1:]['yhat1']
            future_T1.iloc[-1, future_T1.columns.get_loc('T2')] = forecast_future_T2[-1:]['yhat1']
            future_T1.iloc[-1, future_T1.columns.get_loc('probMeas0Prep1')] = forecast_future_Prob0[-1:]['yhat1']
            future_T1.iloc[-1, future_T1.columns.get_loc('probMeas1Prep0')] = forecast_future_Prob1[-1:]['yhat1']
            future_T1.iloc[-1, future_T1.columns.get_loc('readout_error')] = forecast_future_error[-1:]['yhat1']
            
            future_T2.iloc[-1, future_T2.columns.get_loc('T1')] = forecast_future_T1[-1:]['yhat1']
            future_T2.iloc[-1, future_T2.columns.get_loc('y')] = forecast_future_T2[-1:]['yhat1']
            future_T2.iloc[-1, future_T2.columns.get_loc('probMeas0Prep1')] = forecast_future_Prob0[-1:]['yhat1']
            future_T2.iloc[-1, future_T2.columns.get_loc('probMeas1Prep0')] = forecast_future_Prob1[-1:]['yhat1']
            future_T2.iloc[-1, future_T2.columns.get_loc('readout_error')] = forecast_future_error[-1:]['yhat1']

            future_Prob0.iloc[-1, future_Prob0.columns.get_loc('T1')] = forecast_future_T1[-1:]['yhat1']
            future_Prob0.iloc[-1, future_Prob0.columns.get_loc('T2')] = forecast_future_T2[-1:]['yhat1']
            future_Prob0.iloc[-1, future_Prob0.columns.get_loc('y')] = forecast_future_Prob0[-1:]['yhat1']
            future_Prob0.iloc[-1, future_Prob0.columns.get_loc('probMeas1Prep0')] = forecast_future_Prob1[-1:]['yhat1']
            future_Prob0.iloc[-1, future_Prob0.columns.get_loc('readout_error')] = forecast_future_error[-1:]['yhat1']

            future_Prob1.iloc[-1, future_Prob1.columns.get_loc('T1')] = forecast_future_T1[-1:]['yhat1']
            future_Prob1.iloc[-1, future_Prob1.columns.get_loc('T2')] = forecast_future_T2[-1:]['yhat1']
            future_Prob1.iloc[-1, future_Prob1.columns.get_loc('probMeas0Prep1')] = forecast_future_Prob0[-1:]['yhat1']
            future_Prob1.iloc[-1, future_Prob1.columns.get_loc('y')] = forecast_future_Prob1[-1:]['yhat1']
            future_Prob1.iloc[-1, future_Prob1.columns.get_loc('readout_error')] = forecast_future_error[-1:]['yhat1']
            
            future_error.iloc[-1, future_error.columns.get_loc('T2')] = forecast_future_T2[-1:]['yhat1']
            future_error.iloc[-1, future_error.columns.get_loc('probMeas0Prep1')] = forecast_future_Prob0[-1:]['yhat1']
            future_error.iloc[-1, future_error.columns.get_loc('probMeas1Prep0')] = forecast_future_Prob1[-1:]['yhat1']
            future_error.iloc[-1, future_error.columns.get_loc('T1')] = forecast_future_T1[-1:]['yhat1']
            future_error.iloc[-1, future_error.columns.get_loc('y')] = forecast_future_error[-1:]['yhat1']
            
            if i != n_steps - 1:
                future_T1 = model_T1.make_future_dataframe(df=future_T1, n_historic_predictions=True, periods=n_steps)
                future_T2 = model_T2.make_future_dataframe(df=future_T2, n_historic_predictions=True, periods=n_steps)
                future_Prob0 = model_Prob0.make_future_dataframe(df=future_Prob0, n_historic_predictions=True, periods=n_steps)
                future_Prob1 = model_Prob1.make_future_dataframe(df=future_Prob1, n_historic_predictions=True, periods=n_steps)
                future_error = model_error.make_future_dataframe(df=future_error, n_historic_predictions=True, periods=n_steps)

        return future_T1

    except FileNotFoundError:
        raise FileNotFoundError("One of the models is missing")




machines = ['Brisbane', 'Kyoto', 'Osaka']
nPredictions = 36

for machine in machines:
    future_T1 = predict_qubits(nPredictions, machine)

    path = "backend/dataframes_neuralProphet/scalerT1" + machine + ".pkl"

    scaler = joblib.load(path)

    dates = future_T1['ds']
    df_values = future_T1.drop(columns=['ds'])

    inverted_df = scaler.inverse_transform(df_values)

    df = pd.DataFrame(inverted_df, columns=['T1', 'T2', 'prob0', 'prob1', 'error'])
    df['ds'] = dates

    data = df.iloc[-nPredictions:]

    data.to_csv('scripts/experimentos/experimento3/neural/dataframe_experimentNeuralQubits' + machine + '.csv', index=False)

for machine in machines:
    future_T1 = predict_gates(nPredictions, machine)

    data = future_T1.iloc[-nPredictions:]

    data.to_csv('scripts/experimentos/experimento3/neural/dataframe_experimentNeuralGates' + machine + '.csv', index=False)
