from neuralprophet import NeuralProphet, set_log_level
import pandas as pd
import pickle


def create_model(fichero):
    # Se leen los datos
    directorio = 'dataframes/'
    df = pd.read_csv(directorio + fichero, encoding="latin1")
    columns = df.columns.to_list()

    start = fichero.find("dataframe") + len("dataframe")
    end = fichero.find(".csv")
    substring = fichero[start:end]

    # Especifica el índice donde se dividirán los datos (90% entrenamiento, 10% validacion)
    train_index = int(len(df) * 0.8)

    # Dividir el DataFrame en conjuntos de entrenamiento y prueba
    df_train = df.iloc[:train_index]
    df_test = df.iloc[train_index:]

    # Se crea el modelo 
    model = NeuralProphet(
        n_forecasts=1,
        learning_rate=0.1
    )

    set_log_level("ERROR")

    # Se introducen el resto de variables como regresores
    model.add_lagged_regressor(columns[2])
    model.add_lagged_regressor(columns[3])
    model.add_lagged_regressor(columns[4])
    model.add_lagged_regressor(columns[5])

    model.set_plotting_backend("plotly-static")

    metrics = model.fit(df=df_train, freq="H", validation_df=df_test)
    #print(metrics)

    file_name = 'models_neuralProphet/model' + substring + '.pkl'
    with open(file_name, "wb") as file:
        pickle.dump(model, file)


def predict(n_steps, nombreMaquina):
    nombreMaquina = nombreMaquina.split("_")[1].capitalize()
    try:
        directorio = 'models_neuralProphet'
        with open(directorio + 'modelT1' + nombreMaquina + '.pkl', "rb") as file:
            model_T1 = pickle.load(file)
        with open(directorio + 'modelT2' + nombreMaquina + '.pkl', "rb") as file:
            model_T2 = pickle.load(file)
        with open(directorio + 'modelProb0' + nombreMaquina + '.pkl', "rb") as file:
            model_Prob0 = pickle.load(file)
        with open(directorio + 'modelProb1' + nombreMaquina + '.pkl', "rb") as file:
            model_Prob1 = pickle.load(file)
        with open(directorio + 'modelError' + nombreMaquina + '.pkl', "rb") as file:
            model_error = pickle.load(file)
        
        directorio_dataframes = 'dataframes/'

        df_T1 = pd.read_csv(directorio_dataframes + 'dataframeT1' + nombreMaquina + '.csv', encoding="latin1")
        df_T2 = pd.read_csv(directorio_dataframes + 'dataframeT2' + nombreMaquina + '.csv', encoding="latin1")
        df_Prob0 = pd.read_csv(directorio_dataframes + 'dataframeProb0' + nombreMaquina + '.csv', encoding="latin1")
        df_Prob1 = pd.read_csv(directorio_dataframes + 'dataframeProb1' + nombreMaquina + '.csv', encoding="latin1")
        df_error = pd.read_csv(directorio_dataframes + 'dataframeError' + nombreMaquina + '.csv', encoding='latin1')

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
            
            if(i != n_steps - 1):
                future_T1 = model_T1.make_future_dataframe(df=future_T1, n_historic_predictions=True, periods=n_steps)
                future_T2 = model_T2.make_future_dataframe(df=future_T2, n_historic_predictions=True, periods=n_steps)
                future_Prob0 = model_Prob0.make_future_dataframe(df=future_Prob0, n_historic_predictions=True, periods=n_steps)
                future_Prob1 = model_Prob1.make_future_dataframe(df=future_Prob1, n_historic_predictions=True, periods=n_steps)
                future_error = model_error.make_future_dataframe(df=future_error, n_historic_predictions=True, periods=n_steps)

        '''
        model_T1.highlight_nth_step_ahead_of_each_forecast(1)
        model_T1.plot(forecast_future_T1[-12:])
        '''
        return future_T1, future_T2, future_Prob0, future_Prob1, future_error

    except FileNotFoundError:
        raise FileNotFoundError("No se ha encontrado uno de los modelos")


maquinas = ["Brisbane", "Kyoto", "Osaka"] 
ficheros = ["dataframeT1", "dataframeT2", "dataframeProb0", "dataframeProb1", "dataframeError"]

for maquina in maquinas:
    for fichero in ficheros:
        print("Maquina: " + maquina + ", fichero: " + fichero)
        csv = fichero + maquina + '.csv'
        create_model(csv)
print("Modelo creado con éxito")

'''
future_T1, future_T2, future_Prob0, future_Prob1, future_error = predict(4, "ibm_Brisbane")
print(future_T1)
'''



