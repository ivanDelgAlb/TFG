from fastapi import APIRouter, FastAPI, File, Form, UploadFile
from pydantic import BaseModel
from appWeb.predictionsPerceptron import predictQubitsError
from appWeb.predictionsXgBoost import predictGatesError
from appWeb import processFile
from typing import List, Dict, Union
from typing import Optional
import json

router = APIRouter()

class PredictionData(BaseModel):
    machine: str
    selection: str
    t1: Optional[float] = None
    t2: Optional[float] = None
    prob0: Optional[float] = None
    prob1: Optional[float] = None
    readout_error: Optional[float] = None
    depth: Optional[str] = None
    gate_error_1: Optional[float] = None
    gate_error_2: Optional[float] = None



@router.post("/")
async def get_prediction(data: PredictionData) -> Dict[str, List[Dict[str, Union[float, str]]]]:
    if(data.selection == 'Qubits'):
        prediction = {
            "T1": data.t1,
            "T2": data.t2,
            "Prob0": data.prob0,
            "Prob1": data.prob1,
            "Error": data.readout_error
        }
    else: 
        prediction = []
        prediction.append([data.gate_error_1, data.gate_error_2])

    predictions = []
    predictions.append(prediction)

    if(data.selection == 'Qubits'):
        prediction = predictQubitsError.predict_qubits_error(predictions, data.machine, data.depth)
    else: 
        prediction = predictGatesError.predict(data.machine, predictions)

    return {"prediction": prediction}


class CalibrationData(BaseModel):
    selection: str
    depth: Optional[str] = None
    file: UploadFile
    nQubits: int
    tGates: int
    phaseGates: int
    hGates: int
    cNotGates: int

@router.post("/file")
async def get_prediction(data: CalibrationData) -> Dict[str, List[Dict[str, Union[float, str]]]]:
    print("HOLA")
    
    try:

        content = await data.file.read()
        file_data = json.loads(content)
    except Exception as e:
        return{"error": f"Error reading file: {e}"}
    
    name, qubits, gates = processFile.processFile(file_data)

    print("HOLA")

    if(data.selection == 'Qubits'):
        prediction = {
            "T1": qubits[0]['mediana'],
            "T2": qubits[1]['mediana'],
            "Prob0": qubits[2]['mediana'],
            "Prob1": qubits[3]['mediana'],
            "Error": qubits[4]['mediana'],
            "nQubits": data.nQubits,
            "tGates": data.tGates,
            "phaseGates": data.phaseGates,
            "hGates": data.hGates,
            "cnotGates": data.cNotGates,
            "depth": data.depth
        }
    else: 
        prediction = []
        prediction.append([
            gates[0]['mediana'], 
            gates[1]['mediana'], 
            data.nQubits,
            data.tGates,
            data.phaseGates,
            data.hGates,
            data.cNotGates
        ])

    predictions = []
    predictions.append(prediction)

    print(predictions)

    name = name.replace("_", " ")
    
    if(data.selection == 'Qubits'):
        prediction = predictQubitsError.predict_qubits_error(predictions, name, 'calibration')
    else: 
        prediction = predictGatesError.predict(name, predictions)
    print(prediction)
    return {"prediction": prediction}