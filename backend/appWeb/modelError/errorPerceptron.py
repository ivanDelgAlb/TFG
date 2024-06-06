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

from appWeb.predictionsXgBoost import (
    predictQubitsCalibration as predictQubitsCalibrationXgBoost,
    predictQubitsError as predictQubitsErrorXgBoost,
    predictGatesCalibration as predictGatesCalibrationXgBoost,
    predictGatesError as predictGatesErrorXgBoost
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
    model: Optional[str] = None


def predict_qubits(data: PredictionData):
    machines = []
    if data.machine == "All":
        machines = ["ibm brisbane", "ibm kyoto", "ibm osaka"]
    else:
        machines = [data.machine]

    all_predictions = {}
    n_steps = calculate_time_difference(data.date)

    for machine in machines:
        
        future_T1, future_T2, future_Prob0, future_Prob1, future_error = predictGatesCalibrationPerceptron.predict_qubits_calibration(n_steps, machine)

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

    print("Diccionario")
    print(all_predictions)
    return all_predictions


def predict_gates(data: PredictionData):
    print("predict gates")
    n_steps = calculate_time_difference(data.date)
    if data.model == None or data.model == "XgBoost":
        print("Entra")
    else:
        print("A")
    predictions = predictGatesCalibrationXgBoost.predict_future(data.machine, n_steps)
    print(predictions)
    gate_errors_1 = []
    gate_errors_2 = []
    n_qubits = []
    t_gates = []
    h_gates = []
    phase_gates = []
    cnot_gates = []

    for prediction in predictions:
        gate_errors_1.append(prediction[0][0])
        gate_errors_2.append(prediction[0][1])
        n_qubits.append(data.nQubits)
        t_gates.append(data.tGates)
        h_gates.append(data.hGates)
        phase_gates.append(data.phaseGates)
        cnot_gates.append(data.cnotGates)

    gate_errors_1 = np.array(gate_errors_1)
    gate_errors_2 = np.array(gate_errors_2)
    n_qubits = np.array(n_qubits)
    t_gates = np.array(t_gates)
    h_gates = np.array(h_gates)
    phase_gates = np.array(phase_gates)
    cnot_gates = np.array(cnot_gates)

    data_np = np.column_stack((gate_errors_1, gate_errors_2, n_qubits, t_gates, h_gates, phase_gates, cnot_gates))

    print(predictions)
    predictions = predictGatesErrorXgBoost.predict(data.machine, predictions)
    return predictions


def calculate_time_difference(selected_date_str):
    local_timezone = pytz.timezone('Europe/Madrid')
    current_date = datetime.now(local_timezone)  

    selected_date = datetime.fromisoformat(selected_date_str.replace('Z', '+00:00'))

    time_difference = (selected_date - current_date).total_seconds() / 3600

    rounded_hours = round(time_difference / 2) + 1
    return rounded_hours

