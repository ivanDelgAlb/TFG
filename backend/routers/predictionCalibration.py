from fastapi import APIRouter
from pydantic import BaseModel
from appWeb import predictQubitsError
from appWeb import predictGatesError
from typing import List, Dict, Union
from typing import Optional

router = APIRouter()

# Clase para definir la estructura de los datos enviados desde el frontend
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


# Define la ruta para /predict como POST y recibe los datos del cuerpo de la solicitud
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

    # Devolver la predicción
    return {"prediction": prediction}