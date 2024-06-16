from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from appWeb.predictionsPerceptron import predictQubitsErrorPerceptron
from appWeb.predictionsPerceptron import predictGatesErrorPerceptron
from appWeb.predictionsXgBoost import predictQubitsErrorXgBoost
from appWeb.predictionsXgBoost import predictGatesErrorXgBoost
from appWeb import processFile
from typing import List, Dict, Union
from typing import Optional
import json

router = APIRouter()

@router.post("/")
async def get_prediction(
    selection: str = Form(...),
    depth: Optional[str] = Form(None),
    model: str = Form(...),
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
    
    predictions = []
    name = name.replace("_", " ")

    all_predictions = {}

    if model == 'Perceptron-XgBoost' or model == 'Perceptron':
        if(selection == 'Qubits'):
            predictions = []
            prediction = {
                "T1": qubits[0]['mediana'],
                "T2": qubits[1]['mediana'],
                "Prob0": qubits[2]['mediana'],
                "Prob1": qubits[3]['mediana'],
                "Error": qubits[4]['mediana'],
                "nQubits": nQubits,
                "depth": depth,
                "tGates": tGates,
                "phaseGates": phaseGates,
                "hGates": hGates,
                "cnotGates": cNotGates,

            }
            predictions.append(prediction)
            prediction = predictQubitsErrorPerceptron.predict_qubits_error(predictions, name, 'calibration')
            
        else:
            predictions = []
            prediction = {
                "error_gate_1_qubit": gates[0]['mediana'], 
                "error_gate_2_qubit": gates[1]['mediana'], 
                "nQubits": nQubits,
                "tGates": tGates,
                "hGates": hGates,
                "phaseGates": phaseGates,
                "cnotGates": cNotGates,
            }
            predictions.append(prediction)
            prediction = predictGatesErrorPerceptron.predict_gates_error(name, predictions)
            

        prediction[0]['divergence'] = abs(prediction[0]['divergence'])
        all_predictions["Perceptron"] = prediction
    
    if model == 'Perceptron-XgBoost' or model == 'XgBoost':
        if selection == 'Qubits':
            prediction = []
            predictions = []
            prediction.append([
                qubits[0]['mediana'],
                qubits[1]['mediana'],
                qubits[2]['mediana'],
                qubits[3]['mediana'],
                qubits[4]['mediana'],
                nQubits,
                depth,
                tGates,
                phaseGates,
                hGates,
                cNotGates
            ])

            predictions.append(prediction)
            prediction = predictQubitsErrorXgBoost.predict(name, predictions, 'calibration')
        else: 
            predictions = []
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

            predictions.append(prediction)
            prediction = predictGatesErrorXgBoost.predict(name, predictions, 'calibration')

        prediction[0]['divergence'] = abs(prediction[0]['divergence'])
        all_predictions["XgBoost"] = prediction 
    #prediction = predictGatesError.predict(name, predictions, 'calibration')
    
    print(all_predictions)

    return all_predictions