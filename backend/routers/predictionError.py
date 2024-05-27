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
async def predict(data: PredictionData) -> Dict[str, List[Dict[str, Union[float, str]]]]:
    # Aquí realizas la predicción con los datos recibidos
    print("Datos recibidos predict error:", data)
    prediction = None
    
    if data.model.startswith("Perceptron") or data.model == "Perceptron":
        if data.selection == "Qubits":
            prediction = errorPerceptron.predict_qubits(data)
            print(prediction)
        else: 
            prediction = errorPerceptron.predict_puertas(data)

    if data.model.endswith("XgBoost") or data.model == "XgBoost":
        print("ENTRO")
        if data.selection == "Qubits":
            prediction = errorXgboost.predict_qubits(data)
        else:
            prediction = errorXgboost.predict_puertas(data)
    return {"prediction": prediction}
