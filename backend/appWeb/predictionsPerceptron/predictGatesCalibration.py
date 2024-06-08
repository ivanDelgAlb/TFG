import pandas as pd
import pickle
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def predict_gates(machine_name, n_steps):
    """
    Predicts the configuration for a given machine in n_steps (each step is an hour)
    :param n_steps: the number of steps to predict
    :param machine_name: the name of the machine to predict the configuration
    :return: A dataframe with the past data and the predicted ones
    :rtype: pandas.core.frame.DataFrame
    """

    machine_name = machine_name.split(" ")[1].capitalize()

    try:
        if os.getenv("DEPLOYMENT") == 'localhost': models_directory = os.path.join(os.getenv("PATH_FILE"), 'models_neuralProphet/')
        else: models_directory = os.path.join(os.environ['PWD'], 'models_neuralProphet/')
        
        with open(models_directory + 'modelError1' + machine_name + '.pkl', "rb") as file:
            model_error_1 = pickle.load(file)
        with open(models_directory + 'modelError2' + machine_name + '.pkl', "rb") as file:
            model_error_2 = pickle.load(file)

        if os.getenv("DEPLOYMENT") == 'localhost': dataframes_directory = os.path.join(os.getenv("PATH_FILE"), 'dataframes_neuralProphet/')
        else: dataframes_directory = os.path.join(os.environ['PWD'], 'dataframes_neuralProphet/')

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