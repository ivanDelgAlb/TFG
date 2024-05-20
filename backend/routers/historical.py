from typing import List, Dict, Union
from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/")
async def historical():
    historical = []

    qubits = qubitsCalibration()
    gates = gatesCalibration()
    historical.append(qubits)
    historical.append(gates)
        
    return {"historical": historical}

def qubitsCalibration():
    dataframes_directory = 'backend/dataframes_neuralProphet/'
    machines = ['Brisbane', 'Kyoto', 'Osaka']

    # Leer el archivo CSV
    qubits = pd.read_csv(dataframes_directory + 'dataframeT1' + machines[0] + '.csv', encoding="latin1")

    # Cambiar el nombre de la columna
    qubits = qubits.rename(columns={'y': 'T1'})

    # Eliminar una columna
    qubits = qubits.rename(columns={'ds': 'Date'})
    
    return {'qubits': qubits.to_dict(orient='records')} # Convertir DataFrame a lista de diccionarios


def gatesCalibration() -> Dict[str, Union[str, str]]:
    dataframes_directory = 'backend/dataframes_gates/'
    machines = ['Brisbane', 'Kyoto', 'Osaka']

    # Leer el archivo CSV
    gates = pd.read_csv(dataframes_directory + 'dataframe_Gates' + machines[0] + '.csv', encoding="latin1")

    # Eliminar una columna
    gates = gates.drop(columns=['date'])
    
    return {'gates': gates.to_dict(orient='records')}  # Convertir DataFrame a lista de diccionarios
