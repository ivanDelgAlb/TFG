from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import pytz
from appWeb import predictQubitsCalibration
from typing import List, Dict

router = APIRouter()

class PredictionData(BaseModel):
    machine: str
    date: Optional[str] = None
    selection: Optional[str] = None

@router.post("/")
async def predict(data: PredictionData) -> Dict[str, List[Dict[str, float]]]:
    # Aquí realizas la predicción con los datos recibidos
    print("Datos recibidos:", data)
    
    if data.selection == "qubits":
        prediction = predict_qubits(data)
    elif data.selection == "puertas":
        prediction = predict_puertas(data)
    else:
        prediction = None
    
    return {"prediction": prediction}

def predict_qubits(data: PredictionData) -> List[Dict[str, float]]:
    n_steps = calculate_hours_elapsed(data.date) 
    future_T1, future_T2, future_Prob0, future_Prob1, future_error = predictQubitsCalibration.predict_qubits_calibration(n_steps, data.machine)
    
    predictions = []
    for i in range(n_steps):
        prediction = {
            "T1": future_T1.iloc[i, future_T1.columns.get_loc('y')],
            "T2": future_T2.iloc[i, future_T2.columns.get_loc('y')],
            "Prob0": future_Prob0.iloc[i, future_Prob0.columns.get_loc('y')],
            "Prob1": future_Prob1.iloc[i, future_Prob1.columns.get_loc('y')],
            "Error": future_error.iloc[i, future_error.columns.get_loc('y')]
        }
        predictions.append(prediction)

    print(predictions)

    return predictions

def predict_puertas(data: PredictionData):
    # Aquí realizas la predicción específica para puertas
    # Puedes implementar tu lógica aquí
    # Por ejemplo:
    return 0.05  # Esta es solo una predicción de ejemplo


def calculate_hours_elapsed(selected_date_str):
    local_timezone = pytz.timezone('Europe/Madrid')  # Replace 'Europe/Madrid' with your actual local timezone
    current_date = datetime.now(local_timezone)  # Get current time in local timezone
    current_date_utc = current_date.astimezone(pytz.utc)  # Convert local time to UTC
    selected_date = datetime.fromisoformat(selected_date_str.replace('Z', '+00:00'))
    selected_date = selected_date.replace(tzinfo=pytz.utc)  # Make selected date timezone-aware
    time_difference = selected_date - current_date_utc
    hours_elapsed = time_difference.total_seconds() / 3600
    return round(hours_elapsed)

import plotly.graph_objects as go



def plot_calibration_plotly(predictions):
    # Crear un gráfico para cada calibración
    for key, values in predictions.items():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(1, len(values) + 1)), y=values, mode='lines', name=key))
        fig.update_layout(title=f'{key} Calibration Predictions', xaxis_title='Sample', yaxis_title='Prediction')
        fig.show()

