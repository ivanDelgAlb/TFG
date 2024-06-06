from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import pytz
from appWeb.predictionsPerceptron import (
    predictQubitsCalibration as predictQubitsCalibrationPerceptron,
    predictQubitsError as predictQubitsErrorPerceptron,
    predictGatesCalibration as predictGatesCalibrationPerceptron,
    predictGatesError as predictGatesErrorPerceptron
)

from typing import List, Dict, Union
import numpy as np

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


def predict_qubits(data: PredictionData):
    machines = []
    if data.machine == "All":
        machines = ["ibm brisbane", "ibm kyoto", "ibm osaka"]
    else:
        machines = [data.machine]

    all_predictions = {}
    n_steps = calculate_time_difference(data.date)

    for machine in machines:
        
        future_T1, future_T2, future_Prob0, future_Prob1, future_error = predictQubitsCalibrationPerceptron.predict_qubits_calibration(n_steps, machine)

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
                "cnotGates": data.cnotGates,
                "depth": data.depth
            }
            predictions.append(prediction)
        
        predictions = predictQubitsErrorPerceptron.predict_qubits_error(predictions, machine)
        all_predictions[machine] = predictions

    return all_predictions


def predict_gates(data: PredictionData):
    machines = []

    if data.machine == "All":
        machines = ["ibm brisbane", "ibm kyoto", "ibm osaka"]
    else:
        machines = [data.machine]
    all_predictions = {}

    n_steps = calculate_time_difference(data.date)

    for machine in machines:
        future_error_1 = predictGatesCalibrationPerceptron.predict_gates(machine, n_steps)
        predictions = []
        for i in range(n_steps):
            prediction = {
                "error_gate_1_qubit": future_error_1.iloc[i, future_error_1.columns.get_loc('y')],
                "error_gate_2_qubit": future_error_1.iloc[i, future_error_1.columns.get_loc('error_2')],
                "nQubits": data.nQubits,
                "tGates": data.tGates,
                "hGates": data.hGates,
                "phaseGates": data.phaseGates,
                "cnotGates": data.cnotGates
            }
            predictions.append(prediction)

        predictions = predictGatesErrorPerceptron.predict_gates_error(data.machine, predictions)
        all_predictions[machine] = predictions
        
    return all_predictions


def calculate_time_difference(selected_date_str):
    local_timezone = pytz.timezone('Europe/Madrid')
    current_date = datetime.now(local_timezone)  

    selected_date = datetime.fromisoformat(selected_date_str.replace('Z', '+00:00'))

    time_difference = (selected_date - current_date).total_seconds() / 3600

    rounded_hours = round(time_difference / 2) + 1
    return rounded_hours

