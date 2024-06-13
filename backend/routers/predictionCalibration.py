from fastapi import APIRouter, FastAPI, File, Form, UploadFile
from pydantic import BaseModel
from appWeb.predictionsPerceptron import predictQubitsError
from appWeb.predictionsXgBoost import predictGatesError
from appWeb import processFile
from typing import List, Dict, Union
from typing import Optional
import json
import math

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


@router.post("/file")
async def get_prediction(
    selection: str = Form(...),
    depth: Optional[str] = Form(None),
    nQubits: int = Form(...),
    tGates: int = Form(...),
    phaseGates: int = Form(...),
    hGates: int = Form(...),
    cNotGates: int = Form(...),
    file: UploadFile = File(...)
    ) -> Dict[str, List[Dict[str, Union[float, str]]]]:
    try:
        content = await file.read()
        file_data = json.loads(content)
    except Exception as e:
        return{"error": f"Error reading file: {e}"}
    
    name, qubits, gates = processFile.processFile(file_data)

    if(selection == 'Qubits'):
        prediction = {
            "T1": qubits[0]['mediana'],
            "T2": qubits[1]['mediana'],
            "Prob0": qubits[2]['mediana'],
            "Prob1": qubits[3]['mediana'],
            "Error": qubits[4]['mediana'],
            "nQubits": nQubits,
            "tGates": tGates,
            "phaseGates": phaseGates,
            "hGates": hGates,
            "cnotGates": cNotGates,
            "depth": depth
        }
    else: 
        prediction = []
        prediction.append([
            gates[0]['mediana'], 
            gates[1]['mediana'], 
            nQubits,
            tGates,
            phaseGates,
            hGates,
            cNotGates
        ])

    predictions = []
    predictions.append(prediction)

    name = name.replace("_", " ")
    
    if(selection == 'Qubits'):
        prediction = predictQubitsError.predict_qubits_error(predictions, name, 'calibration')
    else: 
        prediction = predictGatesError.predict(name, predictions, 'calibration')
    
    prediction[0]['divergence'] = abs(prediction[0]['divergence'])

    return {"prediction": prediction}