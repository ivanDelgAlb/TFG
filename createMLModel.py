from neuralprophet import NeuralProphet, set_log_level
import pandas as pd
import pickle

df = pd.read_csv("datos.csv", encoding="latin1")

df.columns = df.columns.str.strip()

'''
try:
    with open('model.pkl', "rb") as archivo_modelo:
        model = pickle.load(archivo_modelo)
except FileNotFoundError:
    model = NeuralProphet()
'''

quantiles = [0.05, 0.95]

model = NeuralProphet(n_forecasts=24, learning_rate=0.01, quantiles=quantiles)

set_log_level("ERROR")

model.add_lagged_regressor("T2")
model.add_lagged_regressor("probMeas0Prep1")
model.add_lagged_regressor("probMeas1Prep0")

model.set_plotting_backend("plotly-static")

# df_train, df_test = model.split(df, valid_p, local_split=True)

metrics = model.fit(df=df, freq="H")

forecast = model.predict(df)
model.highlight_nth_step_ahead_of_each_forecast(1)
model.plot(forecast)

model.plot_components(forecast, components=["lagged_regressors"])
model.plot_parameters(components=["lagged_regressors"])

metrics.tail(1)

df_residuals = pd.DataFrame({"ds": df["ds"], "residuals": df["y"] - forecast["yhat1"]})
fig = df_residuals.plot(x="ds", y="residuals", figsize=(10, 6))

with open('model.pkl', "wb") as file:
    pickle.dump(model, file)