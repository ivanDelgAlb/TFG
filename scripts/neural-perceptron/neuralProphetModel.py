from neuralprophet import NeuralProphet, set_log_level
import pandas as pd
import pickle

# Esta funcion seria para los qubits
def create_model(file):
    """
    Creates a NeuralProphet model in the directory models_neuralProphet from the given dataframe
    :param file: A csv dataframe of the data
    :return: None
    """

    directory = 'backend/dataframes_neuralProphet/'
    df = pd.read_csv(directory + file, encoding="latin1")
    columns = df.columns.to_list()

    start = file.find("dataframe") + len("dataframe")
    end = file.find(".csv")
    substring = file[start:end]

    # Divide the dataframe in training and test
    train_index = int(len(df) * 0.8)
    df_train = df.iloc[:train_index]
    df_test = df.iloc[train_index:]

    # Creating the NeuralProphet model
    model = NeuralProphet(
        n_forecasts=1,
        learning_rate=0.1
    )

    set_log_level("ERROR")

    # Adding the other values as lagged regressors
    model.add_lagged_regressor(columns[2])
    model.add_lagged_regressor(columns[3])
    model.add_lagged_regressor(columns[4])
    model.add_lagged_regressor(columns[5])

    model.set_plotting_backend("plotly-static")

    metrics = model.fit(df=df_train, freq="2H", validation_df=df_test)
    #print(metrics)

    # Saving the model
    file_name = 'backend/models_neuralProphet/model' + substring + '.pkl'
    with open(file_name, "wb") as file:
        pickle.dump(model, file)


def predict(n_steps, machine_name):
    """
    Predicts the configuration for a given machine in n_steps (each step is an hour)
    :param n_steps: the number of steps to predict
    :param machine_name: the name of the machine to predict the configuration
    :return: A dataframe with the past data and the predicted ones
    :rtype: pandas.core.frame.DataFrame
    """

    machine_name = machine_name.split("_")[1].capitalize()

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

        # Take the dataframes_neuralProphet
        df_T1 = pd.read_csv(dataframes_directory + 'dataframeT1' + machine_name + '.csv', encoding="latin1")
        df_T2 = pd.read_csv(dataframes_directory + 'dataframeT2' + machine_name + '.csv', encoding="latin1")
        df_Prob0 = pd.read_csv(dataframes_directory + 'dataframeProb0' + machine_name + '.csv', encoding="latin1")
        df_Prob1 = pd.read_csv(dataframes_directory + 'dataframeProb1' + machine_name + '.csv', encoding="latin1")
        df_error = pd.read_csv(dataframes_directory + 'dataframeError' + machine_name + '.csv', encoding='latin1')

        # Restore the trainers of the models
        model_T1.restore_trainer()
        model_T2.restore_trainer()
        model_Prob0.restore_trainer()
        model_Prob1.restore_trainer()
        model_error.restore_trainer()

        # Create a future dataframe to predict the next step
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

        '''
        model_T1.highlight_nth_step_ahead_of_each_forecast(1)
        model_T1.plot(forecast_future_T1[-12:])
        '''
        return future_T1

    except FileNotFoundError:
        raise FileNotFoundError("One of the models is missing")


'''
machines = ["Brisbane", "Kyoto", "Osaka"]
files = ["dataframeT1", "dataframeT2", "dataframeProb0", "dataframeProb1", "dataframeError"]

for machine in machines:
    for file in files:
        print("Maquina: " + machine + ", fichero: " + file)
        csv = file + machine + '.csv'
        create_model(csv)
print("Models created")
'''
from sklearn.preprocessing import MinMaxScaler
import joblib

future_T1 = predict(4, "ibm_Brisbane")

path = "backend/dataframes_neuralProphet/scalerT1Brisbane.pkl"

scaler = joblib.load(path)

dates = future_T1['ds']
df_values = future_T1.drop(columns=['ds'])

inverted_df = scaler.inverse_transform(df_values)

df = pd.DataFrame(inverted_df, columns=['T1', 'T2', 'prob0', 'prob1', 'error'])
df['ds'] = dates

print(df)





