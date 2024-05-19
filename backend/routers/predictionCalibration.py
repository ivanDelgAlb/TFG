from fastapi import APIRouter
from pydantic import BaseModel
from appWeb import predictQubitsError
from typing import List, Dict, Union

router = APIRouter()

# Clase para definir la estructura de los datos enviados desde el frontend
class PredictionData(BaseModel):
    machine: str
    t1: float
    t2: float
    prob0: float
    prob1: float
    readout_error: float
    depth: str


# Define la ruta para /predict como POST y recibe los datos del cuerpo de la solicitud
@router.post("/")
async def get_prediction(data: PredictionData) -> Dict[str, List[Dict[str, Union[float, str]]]]:

    prediction = {
        "T1": data.t1,
        "T2": data.t2,
        "Prob0": data.prob0,
        "Prob1": data.prob1,
        "Error": data.readout_error
    }

    predictions = []
    predictions.append(prediction)

    prediction = predictQubitsError.predict_qubits_error(predictions, data.machine, data.depth)
    print(prediction)
    # Devolver la predicción
    return {"prediction": prediction}