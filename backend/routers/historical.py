from typing import List, Dict, Union
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel
import joblib

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
        
    return {"historical": historical}

def qubitsCalibration(machine):
    dataframes_directory = 'backend/dataframes_neuralProphet/'
    machine = machine.split(" ")[1].capitalize()

    # Leer el archivo CSV
    qubits = pd.read_csv(dataframes_directory + 'dataframeT1' + machine + '.csv', encoding="latin1")

    # Cambiar el nombre de las columnas
    qubits = qubits.rename(columns={'y': 'T1', 'ds': 'Date'})
    fechas = qubits['Date']

    # Seleccionar solo las columnas a desnormalizar
    columns_to_inverse = ['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_error']
    qubits_to_inverse = qubits[columns_to_inverse]

    # Cargar el scaler
    scaler = joblib.load(f"{dataframes_directory}scalerT1{machine}.pkl")

    # Desnormalizar los datos
    qubits_desnormalized = scaler.inverse_transform(qubits_to_inverse)

    # Convertir el array desnormalizado a un DataFrame
    qubits_desnormalized = pd.DataFrame(qubits_desnormalized, columns=columns_to_inverse)

    # Agregar la columna 'Date'
    qubits_desnormalized['Date'] = fechas

    qubits_desnormalized = qubits_desnormalized.rename(columns={'probMeas0Prep1': 'Prob0', 'probMeas1Prep0': 'Prob1', 'readout_error': 'Error'})

    return {'qubits': qubits_desnormalized.to_dict(orient='records')} # Convertir DataFrame a lista de diccionarios



def gatesCalibration(machine) -> Dict[str, Union[str, str]]:
    dataframes_directory = 'backend/dataframes_gates/'
    machine = machine.split(" ")[1].capitalize()

    # Leer el archivo CSV
    gates = pd.read_csv(dataframes_directory + 'dataframe_Gates' + machine + '.csv', encoding="latin1")

    fechas = gates['date']

    # Seleccionar solo las columnas a desnormalizar
    columns_to_inverse = ['gate_error_1','gate_error_2']
    gates_to_inverse = gates[columns_to_inverse]

    # Cargar el scaler
    scaler = joblib.load(f"{dataframes_directory}scalerGates{machine}.pkl")

    # Desnormalizar los datos
    gates_desnormalized = scaler.inverse_transform(gates_to_inverse)

    # Convertir el array desnormalizado a un DataFrame
    gates_desnormalized = pd.DataFrame(gates_desnormalized, columns=columns_to_inverse)

    # Agregar la columna 'Date'
    gates_desnormalized['Date'] = fechas


    print(gates_desnormalized)
    
    return {'gates': gates_desnormalized.to_dict(orient='records')}  # Convertir DataFrame a lista de diccionarios

def errorQubits(machine) -> Dict[str, Union[str, str]]:
    dataframes_directory = 'backend/dataframes_perceptron/'
    machine = machine.split(" ")[1].capitalize()

    # Leer el archivo CSV
    errorQubits = pd.read_csv(dataframes_directory + 'dataframe_perceptron_qubits_' + machine + '.csv', encoding="latin1")

    # Cambiar el nombre de la columna
    errorQubits = errorQubits.rename(columns={'date': 'Date', 'jensen-error': 'jensen_error'})

    errorQubits = errorQubits.drop(['T1','T2','probMeas0Prep1','probMeas1Prep0','readout_qubit_error','n_qubits','depth','t_gates','phase_gates','h_gates','cnot_gates','kullback_error'], axis=1)

    print(errorQubits)
    
    return {'errorQubits': errorQubits.to_dict(orient='records')}  # Convertir DataFrame a lista de diccionarios

def errorGates(machine) -> Dict[str, Union[str, str]]:
    dataframes_directory = 'backend/dataframes_xgboost/'
    machine = machine.split(" ")[1].capitalize()

    # Leer el archivo CSV
    errorGates = pd.read_csv(dataframes_directory + 'dataframe_perceptron_gates_' + machine + '.csv', encoding="latin1")

    # Cambiar el nombre de la columna
    errorGates = errorGates.rename(columns={'date': 'Date', 'jensen-error': 'jensen_error'})

    errorGates = errorGates.drop(['gate_error_one_qubit','gate_error_two_qubit','n_qubits','t_gates','phase_gates','h_gates','cnot_gates','kullback_error'], axis=1)
    errorGates = errorGates.notna()

    print(errorGates)
    
    return {'errorGates': errorGates.to_dict(orient='records')}  # Convertir DataFrame a lista de diccionarios

