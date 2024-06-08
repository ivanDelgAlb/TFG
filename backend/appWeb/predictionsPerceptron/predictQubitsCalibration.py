import pandas as pd
import pickle
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def predict_qubits_calibration(n_steps, machine_name):
    """
    Predicts the configuration for a given machine in n_steps (each step is an hour)
    :param n_steps: Number of steps to predict
    :param machine_name: Name of the machine to predict the configuration
    :return: Dataframe with the past data and the predicted ones
    :rtype: pandas.core.frame.DataFrame
    """

    machine_name = machine_name.split(" ")[1].capitalize()

    try:
        if os.getenv("DEPLOYMENT") == 'localhost': models_directory = os.path.join(os.getenv("PATH_FILE"), 'models_neuralProphet/')
        else: models_directory = os.path.join(os.environ['PWD'], 'models_neuralProphet/')

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

        if os.getenv("DEPLOYMENT") == 'localhost': dataframes_directory = os.path.join(os.getenv("PATH_FILE"), 'dataframes_neuralProphet/')
        else: dataframes_directory = os.path.join(os.environ['PWD'], 'dataframes_neuralProphet/')

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

        return future_T1, future_T2, future_Prob0, future_Prob1, future_error

    except FileNotFoundError:
        raise FileNotFoundError("One of the models is missing")



