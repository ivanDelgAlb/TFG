from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
import pytz
from appWeb import predictQubitsCalibration
from appWeb import predictQubitsError
from appWeb import predictGatesCalibration
from appWeb import predictGatesError
from typing import List, Dict, Union
import numpy as np

router = APIRouter()

class PredictionData(BaseModel):
    machine: str
    date: str
    selection: str
    depth: Optional[str] = None
    nQubits: float
    tGates: float
    hGates: float
    phaseGates: float
    cnotGates: float


@router.post("/")
async def predict(data: PredictionData) -> Dict[str, List[Dict[str, Union[float, str, str, str, str, str, str]]]]:
    # Aquí realizas la predicción con los datos recibidos
    print("Datos recibidos predict error:", data)
    
    if data.selection == "Qubits":
        prediction = predict_qubits(data)
    elif data.selection == "Gates":
        prediction = predict_puertas(data)
    else:
        prediction = None
        
    return {"prediction": prediction}

def predict_qubits(data: PredictionData) -> List[Dict[str, Union[float, str, str, str, str, str, str]]]:

    n_steps = calculate_time_difference(data.date) 
    future_T1, future_T2, future_Prob0, future_Prob1, future_error = predictQubitsCalibration.predict_qubits_calibration(n_steps, data.machine)
    
    predictions = []
    for i in range(n_steps):
        prediction = {
            "T1": future_T1.iloc[i, future_T1.columns.get_loc('y')],
            "T2": future_T2.iloc[i, future_T2.columns.get_loc('y')],
            "Prob0": future_Prob0.iloc[i, future_Prob0.columns.get_loc('y')],
            "Prob1": future_Prob1.iloc[i, future_Prob1.columns.get_loc('y')],
            "Error": future_error.iloc[i, future_error.columns.get_loc('y')],
            "nQubits": data.nQubits,
            "tGates": data.tGates,
            "hGates": data.hGates,
            "phaseGates": data.phaseGates,
            "cnotGates": data.cnotGates

        }
        predictions.append(prediction)

    predictions = predictQubitsError.predict_qubits_error(predictions, data.machine, data.depth)
    print("Diccionario")
    print(predictions)
    return predictions


def predict_puertas(data: PredictionData):
    print("predict puertas")
    n_steps = calculate_time_difference(data.date)
    predictions = predictGatesCalibration.predict_future(data.machine, n_steps)
    print(predictions)
    gate_errors_1 = []
    gate_errors_2 = []
    n_qubits = []
    t_gates = []
    h_gates = []
    phase_gates = []
    cnot_gates = []

    # Iterar sobre los diccionarios en predictions para extraer los valores de cada característica
    for prediction in predictions:
        gate_errors_1.append(prediction[0][0])
        gate_errors_2.append(prediction[0][1])
        n_qubits.append(data.nQubits)
        t_gates.append(data.tGates)
        h_gates.append(data.hGates)
        phase_gates.append(data.phaseGates)
        cnot_gates.append(data.cnotGates)

    # Convertir las listas a matrices NumPy
    gate_errors_1 = np.array(gate_errors_1)
    gate_errors_2 = np.array(gate_errors_2)
    n_qubits = np.array(n_qubits)
    t_gates = np.array(t_gates)
    h_gates = np.array(h_gates)
    phase_gates = np.array(phase_gates)
    cnot_gates = np.array(cnot_gates)

    # Combinar todas las matrices NumPy en una sola matriz de características
    data_np = np.column_stack((gate_errors_1, gate_errors_2, n_qubits, t_gates, h_gates, phase_gates, cnot_gates))

    print(predictions)
    predictions = predictGatesError.predict(data.machine, predictions)
    return predictions


def calculate_time_difference(selected_date_str):
    local_timezone = pytz.timezone('Europe/Madrid')  # Reemplaza 'Europe/Madrid' con tu zona horaria local real
    current_date = datetime.now(local_timezone)  # Obtener la hora actual en la zona horaria local

    # Convertir la fecha seleccionada de cadena ISO a datetime
    selected_date = datetime.fromisoformat(selected_date_str.replace('Z', '+00:00'))

    # Calcular la diferencia de tiempo en horas
    time_difference = (selected_date - current_date).total_seconds() / 3600
    
    # Redondear la cantidad de horas al múltiplo de 2 más cercano
    rounded_hours = round(time_difference / 2) + 1
    return rounded_hours

