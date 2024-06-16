from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import pytz
from appWeb.predictionsXgBoost import predictQubitsCalibration
from appWeb.predictionsXgBoost import predictQubitsErrorXgBoost
from appWeb.predictionsXgBoost import predictGatesCalibration
from appWeb.predictionsXgBoost import predictGatesErrorXgBoost
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



def predict_qubits(data: PredictionData) -> List[Dict[str, Union[float, str, str, str, str, str, str]]]:

    if data.machine == "All":
        machines = ["ibm brisbane", "ibm kyoto", "ibm osaka"]
    else:
        machines = [data.machine]

    all_predictions = {}
    n_steps = calculate_time_difference(data.date)
    for machine in machines:
        predictions = predictQubitsCalibration.predict_future(machine, n_steps)
        
        predictions = np.array(predictions)

        predictions[predictions < 0] = 0
        t1 = []
        t2 = []
        prob0 = []
        prob1 = []
        readout_error = []
        n_qubits = []
        depth = []
        t_gates = []
        h_gates = []
        phase_gates = []
        cnot_gates = []

        for prediction in predictions:
            t1.append(prediction[0][0])
            t2.append(prediction[0][1])
            prob0.append(prediction[0][2])
            prob1.append(prediction[0][3])
            readout_error.append(prediction[0][4])
            n_qubits.append(data.nQubits)
            depth.append(data.depth)
            t_gates.append(data.tGates)
            h_gates.append(data.hGates)
            phase_gates.append(data.phaseGates)
            cnot_gates.append(data.cnotGates)

        T1 = np.array(t1)
        T2 = np.array(t2)
        Prob0 = np.array(prob0)
        Prob1 = np.array(prob1)
        Error = np.array(readout_error)
        n_qubits = np.array(n_qubits)
        depth = np.array(depth)
        t_gates = np.array(t_gates)
        h_gates = np.array(h_gates)
        phase_gates = np.array(phase_gates)
        cnot_gates = np.array(cnot_gates)

        predictions = np.column_stack((T1, T2, Prob0, Prob1, Error, n_qubits, depth, t_gates, h_gates, phase_gates, cnot_gates))

        predictions = predictQubitsErrorXgBoost.predict(machine, predictions, 'error')
        all_predictions[machine] = predictions

    return all_predictions


def predict_gates(data: PredictionData):
    if data.machine == "All":
        machines = ["ibm brisbane", "ibm kyoto", "ibm osaka"]
    else:
        machines = [data.machine]
    
    all_predictions = {}
    n_steps = calculate_time_difference(data.date)
    for machine in machines:
        predictions = predictGatesCalibration.predict_future(machine, n_steps)
        predictions = np.array(predictions)
        predictions[predictions < 0] = 0
        
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

        predictions = np.column_stack((gate_errors_1, gate_errors_2, n_qubits, t_gates, h_gates, phase_gates, cnot_gates))

        predictions = predictGatesErrorXgBoost.predict(machine, predictions, 'error')
        all_predictions[machine] = predictions

    return all_predictions


def calculate_time_difference(selected_date_str):
    local_timezone = pytz.timezone('Europe/Madrid')
    current_date = datetime.now(local_timezone)

    selected_date = datetime.fromisoformat(selected_date_str.replace('Z', '+00:00'))

    time_difference = (selected_date - current_date).total_seconds() / 3600
    
    rounded_hours = round(time_difference / 2) + 1
    return rounded_hours

