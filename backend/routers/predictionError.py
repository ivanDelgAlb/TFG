from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from appWeb.modelError import errorPerceptron
from appWeb.modelError import errorXgboost
from typing import List, Dict, Union

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
    model: str


@router.post("/")
async def predict(data: PredictionData) -> Dict[str, Dict[str, List[Dict[str, Union[float, str]]]]]:
    all_predictions = {}
    
    if data.model == "Perceptron-XgBoost" or data.model == "Perceptron":
        if data.selection == "Qubits":
            prediction = errorPerceptron.predict_qubits(data)
        elif data.selection == 'Gates': 
            prediction = errorPerceptron.predict_gates(data)
            
        all_predictions["Perceptron"] = prediction

    if data.model == "Perceptron-XgBoost" or data.model == "XgBoost":
        if data.selection == "Qubits":
            prediction = errorXgboost.predict_qubits(data)
        else:
            prediction = errorXgboost.predict_gates(data)

        all_predictions["XgBoost"] = prediction    
    
    return all_predictions

