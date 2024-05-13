from fastapi import APIRouter
from pydantic import BaseModel
from keras.models import load_model
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

router = APIRouter()

# Clase para definir la estructura de los datos enviados desde el frontend
class PredictionData(BaseModel):
    machine: str
    t1: float
    t2: float
    prob0: float
    prob1: float
    readout_error: float
    date: str


def normalized(t1, t2, prob0, prob1, readout_error):
    fila_min = min(t1, t2, prob0, prob1, readout_error)
    fila_max = max(t1, t2, prob0, prob1, readout_error)

    T1_norm = (t1 - fila_min) / (fila_max - fila_min)
    T2_norm = (t2 - fila_min) / (fila_max - fila_min)
    probMeas0Prep1_norm = (prob0 - fila_min) / (fila_max - fila_min)
    probMeas1Prep0_norm = (prob1 - fila_min) / (fila_max - fila_min)
    readout_error_norm = (readout_error - fila_min) / (fila_max - fila_min)

    df = pd.DataFrame([[T1_norm, T2_norm, probMeas0Prep1_norm, probMeas1Prep0_norm, readout_error_norm]], columns=['T1', 'T2', 'prob0', 'prob1', 'readout_error'])
    return df


# Función de predicción
def predict(machine, t1, t2, prob0, prob1, readout_error):
    # Cargar el modelo correspondiente a la máquina seleccionada
    model = load_model(f'TFG/models_perceptron/model_Brisbane.h5')
    df = normalized(t1, t2, prob0, prob1, readout_error)
    # Realizar la predicción
    prediction = model.predict(df)
    # Convertir la predicción a un valor único (suponiendo que el modelo produce un solo valor)
    prediction_value = prediction[0][0] 
    print(prediction_value)
    return prediction_value

# Define la ruta para /predict como POST y recibe los datos del cuerpo de la solicitud
@router.post("/")
async def get_prediction(data: PredictionData):
    # Obtener los datos de la solicitud
    machine = data.machine
    t1 = data.t1
    t2 = data.t2
    prob0 = data.prob0
    prob1 = data.prob1
    readout_error = data.readout_error
    # Llamar a la función de predicción
    prediction = predict(machine, t1, t2, prob0, prob1, readout_error)
    print(prediction)
    # Devolver la predicción
    return {"prediction": float(prediction)}