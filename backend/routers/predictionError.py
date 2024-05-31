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
    # Aquí realizas la predicción con los datos recibidos
    print("Datos recibidos predict error:", data)
    all_predictions = {}
    
    if data.model.startswith("Perceptron") or data.model == "Perceptron":
        if data.selection == "Qubits":
            prediction = errorPerceptron.predict_qubits(data)
        elif data.selection == 'Gates': 
            prediction = errorPerceptron.predict_puertas(data)
            
        all_predictions["Perceptron"] = prediction

    if data.model.endswith("XgBoost") or data.model == "XgBoost":
        if data.selection == "Qubits":
            prediction = errorXgboost.predict_qubits(data)
        else:
            prediction = errorXgboost.predict_puertas(data)

        all_predictions["XgBoost"] = prediction    

    return all_predictions

