from typing import List, Dict, Union
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel

router = APIRouter()

# Clase para definir la estructura de los datos enviados desde el frontend
class PredictionData(BaseModel):
    machine: str

@router.post("/")
async def historical(data: PredictionData):
    print(data.machine)
    historical = []

    qubits = qubitsCalibration(data.machine)
    gates = gatesCalibration(data.machine)
    historical.append(qubits)
    historical.append(gates)
        
    return {"historical": historical}

def qubitsCalibration(machine):
    dataframes_directory = 'backend/dataframes_neuralProphet/'
    machine = machine.split(" ")[1].capitalize()

    # Leer el archivo CSV
    qubits = pd.read_csv(dataframes_directory + 'dataframeT1' + machine + '.csv', encoding="latin1")

    # Cambiar el nombre de la columna
    qubits = qubits.rename(columns={'y': 'T1'})

    # Cambiar el nombre de la columna
    qubits = qubits.rename(columns={'ds': 'Date'})
    
    return {'qubits': qubits.to_dict(orient='records')} # Convertir DataFrame a lista de diccionarios


def gatesCalibration(machine) -> Dict[str, Union[str, str]]:
    dataframes_directory = 'backend/dataframes_gates/'
    machine = machine.split(" ")[1].capitalize()

    # Leer el archivo CSV
    gates = pd.read_csv(dataframes_directory + 'dataframe_Gates' + machine + '.csv', encoding="latin1")

    # Cambiar el nombre de la columna
    gates = gates.rename(columns={'date': 'Date'})

    print(gates)
    
    return {'gates': gates.to_dict(orient='records')}  # Convertir DataFrame a lista de diccionarios
