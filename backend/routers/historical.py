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
    historical = []

    qubits = qubitsCalibration(data.machine)
    gates = gatesCalibration(data.machine)
    qubitsError = errorQubits(data.machine)
    gatesError = errorGates(data.machine)
    historical.append(qubits)
    historical.append(gates)
    historical.append(qubitsError)
    historical.append(gatesError)

    print(historical)
        
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

def errorQubits(machine) -> Dict[str, Union[str, str]]:
    dataframes_directory = 'backend/dataframes_perceptron/'
    machine = machine.split(" ")[1].capitalize()

    # Leer el archivo CSV
    errorQubits = pd.read_csv(dataframes_directory + 'dataframe_perceptron_qubits_' + machine + '.csv', encoding="latin1")

    # Cambiar el nombre de la columna
    errorQubits = errorQubits.rename(columns={'date': 'Date'})

    errorQubits = errorQubits.drop(['T1','T2','probMeas0Prep1','probMeas1Prep0','readout_qubit_error','n_qubits','depth','t_gates','phase_gates','h_gates','cnot_gates','kullback_error'], axis=1)

    print(errorQubits)
    
    return {'errorQubits': errorQubits.to_dict(orient='records')}  # Convertir DataFrame a lista de diccionarios

def errorGates(machine) -> Dict[str, Union[str, str]]:
    dataframes_directory = 'backend/dataframes_xgboost/'
    machine = machine.split(" ")[1].capitalize()

    # Leer el archivo CSV
    errorGates = pd.read_csv(dataframes_directory + 'dataframe_perceptron_gates_' + machine + '.csv', encoding="latin1")

    # Cambiar el nombre de la columna
    errorGates = errorGates.rename(columns={'date': 'Date'})

    errorGates = errorGates.drop(['gate_error_one_qubit','gate_error_two_qubit','n_qubits','t_gates','phase_gates','h_gates','cnot_gates','kullback_error'], axis=1)
    errorGates = errorGates.notna()

    print(errorGates)
    
    return {'errorGates': errorGates.to_dict(orient='records')}  # Convertir DataFrame a lista de diccionarios

