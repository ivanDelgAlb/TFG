from neuralprophet import NeuralProphet, set_log_level
import pandas as pd
import pickle

# Se leen los datos
df = pd.read_csv("datos.csv", encoding="latin1")

# Especifica el índice donde se dividirán los datos (90% entrenamiento, 10% validacion)
train_index = int(len(df) * 0.9)

# Dividir el DataFrame en conjuntos de entrenamiento y prueba
df_train = df.iloc[:train_index]
df_test = df.iloc[train_index:]

'''
try:
    with open('model.pkl', "rb") as archivo_modelo:
        model = pickle.load(archivo_modelo)
except FileNotFoundError:
    model = NeuralProphet()
'''

# Se crea el modelo 
model = NeuralProphet(
    n_forecasts=12,
    learning_rate=0.01,
    quantiles=[0.05, 0.95]
)

set_log_level("ERROR")

# Se introducen el resto de variables como regresores
model.add_lagged_regressor("T2")
model.add_lagged_regressor("probMeas0Prep1")
model.add_lagged_regressor("probMeas1Prep0")
model.add_lagged_regressor("readout_error")

model.set_plotting_backend("plotly-static")

metrics = model.fit(df=df_train, freq="2H", validation_df=df_test)

# Se crea un dataframe de 12 periodos (24 horas) para predecir los datos del siguiente día
future = model.make_future_dataframe(df, n_historic_predictions=True, periods=12)
forecast_future = model.predict(future)
model.highlight_nth_step_ahead_of_each_forecast(1)
model.plot(forecast_future[-24:])

'''
model.plot_components(forecast, components=["lagged_regressors"])
model.plot_parameters(components=["lagged_regressors"])

df_residuals = pd.DataFrame({"ds": df["ds"], "residuals": df["y"] - forecast["yhat1"]})
fig = df_residuals.plot(x="ds", y="residuals", figsize=(10, 6))
'''

# Se guarda el modelo en un archivo pkl
with open('model.pkl', "wb") as file:
    pickle.dump(model, file)