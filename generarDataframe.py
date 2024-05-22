import pandas as pd
import json
import os
from itertools import repeat


def extract_dataframe(backend_name):
    # Extraer el nombre del archivo JSON
    name = backend_name.split("_")[1].capitalize()

    # Leer los datos de los archivos JSON
    with open(name + "Full.json", "r") as file:
        data = json.load(file)

    with open(name + "2.json", "r") as file:
        data.extend(json.load(file))

    # Definir las columnas para los DataFrames
    qubits_columns = ['T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_qubit_error', 'n_qubits', 'depth', 'kullback_error', 'jensen-error']
    gates_columns = ['gate_error_one_qubit', 'gate_error_two_qubit', 'kullback_error', 'jensen-error', 'n_gates']

    # Crear listas para almacenar los datos
    qubits_data = []
    gates_data = []

    # Extraer los datos
    qubits = [5, 10, 15]
    depths = [5, 10, 15]

    for item in data:
        for qubit in qubits:
            for depth in depths:
                qubits_data.append([
                    item['properties']['qubits'][i]['mediana'] for i in range(5)
                ] + [qubit, depth, "", ""]
                )

        gates_data.extend([
            [item['properties']['gates'][i]['mediana'] for i in range(2)] + ["", "", ""] for _ in range(12)
        ])

    # Convertir las listas de datos a DataFrames de pandas
    df_qubits = pd.DataFrame(qubits_data, columns=qubits_columns)
    df_gates = pd.DataFrame(gates_data, columns=gates_columns)

    # Eliminar duplicados de las puertas (gates)
    df_gates.drop_duplicates(inplace=True)

    # Replicar filas para las puertas (gates)
    replicated_data = pd.concat([df_gates] * 12, ignore_index=True)

    # Definir nombres de archivos CSV
    qubits_csv_file = 'dataframe_perceptron_qubits_' + name + '.csv'
    gates_csv_file = 'dataframe_perceptron_gates_' + name + '.csv'

    # Leer los archivos CSV existentes si existen
    if os.path.exists(qubits_csv_file):
        existing_qubits_data = pd.read_csv(qubits_csv_file)
    else:
        existing_qubits_data = pd.DataFrame(columns=qubits_columns)

    if os.path.exists(gates_csv_file):
        existing_gates_data = pd.read_csv(gates_csv_file)
    else:
        existing_gates_data = pd.DataFrame(columns=gates_columns)

    # Concatenar los nuevos datos con los datos existentes
    final_qubits_data = pd.concat([df_qubits, existing_qubits_data], ignore_index=True)
    final_gates_data = pd.concat([existing_gates_data, replicated_data], ignore_index=True)

    # Guardar los DataFrames como archivos CSV
    final_qubits_data.to_csv(qubits_csv_file, index=False)
    final_gates_data.to_csv(gates_csv_file, index=False)

    print(f"Archivos CSV creados: {qubits_csv_file}, {gates_csv_file}")


# Ejemplo de uso
extract_dataframe("ibm_brisbane")
extract_dataframe("ibm_kyoto")
extract_dataframe("ibm_osaka")
