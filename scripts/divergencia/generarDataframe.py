import pandas as pd
import json
import os

def extract_dataframe(backend_name):
    name = backend_name.split("_")[1].capitalize()

    with open(name + "Full.json", "r") as file:
        data = json.load(file)

    # with open(name + "2.json", "r") as file:
    #     data.extend(json.load(file))

    qubits_columns = ['date', 'T1', 'T2', 'probMeas0Prep1', 'probMeas1Prep0', 'readout_qubit_error', 'n_qubits', 'depth', 't_gates', 'phase_gates', 'h_gates', 'cnot_gates', 'kullback_error', 'jensen-error']
    gates_columns = ['date', 'gate_error_one_qubit', 'gate_error_two_qubit', 'n_qubits', 't_gates', 'phase_gates', 'h_gates', 'cnot_gates', 'kullback_error', 'jensen-error']

    qubits_data = []
    gates_data = []

    qubits = [5, 10, 15]
    depths = [5, 10, 15]

    for item in data:
        for qubit in qubits:
            for depth in depths:
                qubits_data.append([item['date']] + 
                    [item['properties']['qubits'][i]['mediana'] for i in range(5)] + 
                    [qubit, depth, "", "", "", "", "", ""]
                )

        gates_data.extend([
            [item['date']] + [item['properties']['gates'][i]['mediana'] for i in range(2)] + ["", "", "", "", "", "", ""] for _ in range(12)
        ])

    df_qubits = pd.DataFrame(qubits_data, columns=qubits_columns)
    df_gates = pd.DataFrame(gates_data, columns=gates_columns)

    columns_to_consider = [col for col in df_qubits.columns if col != 'date']

    df_gates.drop_duplicates(inplace=True)
    df_qubits.drop_duplicates(inplace=True, subset=columns_to_consider)

    replicated_data = pd.concat([df_gates] * 12, ignore_index=True)

    qubits_csv_file = 'dataframe_perceptron_qubits_' + name + '.csv'
    gates_csv_file = 'dataframe_perceptron_gates_' + name + '.csv'

    if os.path.exists(qubits_csv_file):
        existing_qubits_data = pd.read_csv(qubits_csv_file)
    else:
        existing_qubits_data = pd.DataFrame(columns=qubits_columns)

    if os.path.exists(gates_csv_file):
        existing_gates_data = pd.read_csv(gates_csv_file)
    else:
        existing_gates_data = pd.DataFrame(columns=gates_columns)

    final_qubits_data = pd.concat([df_qubits, existing_qubits_data], ignore_index=True)
    final_gates_data = pd.concat([existing_gates_data, replicated_data], ignore_index=True)

    final_qubits_data.to_csv(qubits_csv_file, index=False)
    final_gates_data.to_csv(gates_csv_file, index=False)

    (f"Archivos CSV creados: {qubits_csv_file}, {gates_csv_file}")


extract_dataframe("ibm_brisbane")
extract_dataframe("ibm_kyoto")
extract_dataframe("ibm_osaka")
