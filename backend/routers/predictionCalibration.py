from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from appWeb.predictionsPerceptron import predictQubitsError
from appWeb.predictionsXgBoost import predictGatesError
from appWeb import processFile
from typing import List, Dict, Union
from typing import Optional
import json

router = APIRouter()

@router.post("/")
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
        name, qubits, gates = processFile.processFile(file_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {e}")
    
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