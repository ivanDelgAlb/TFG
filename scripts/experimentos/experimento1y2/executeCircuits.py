from calculateNoiseError import calculate_configuration_qubit_error, calculate_configuration_gate_error
from generateCircuit import generate_circuit
from qiskit_ibm_runtime import QiskitRuntimeService
import pandas as pd
import time
from qiskit.converters import circuit_to_dag


def count_gates(op_nodes):
    t_gates = 0
    phase_gates = 0
    h_gates = 0
    cnot_gates = 0

    for node in op_nodes:
        if node.name == 't':
            t_gates += 1
        elif node.name == 'p':
            phase_gates += 1
        elif node.name == 'h':
            h_gates += 1
        else:
            cnot_gates += 1
    return t_gates, phase_gates, h_gates, cnot_gates


def execute_qubit_circuit(backend_name):
    service = QiskitRuntimeService(channel='ibm_quantum',
                                   token='d3376e5cf0f14a564e1546bf94465aafdf92db3deb480f4a8b7fe0df18d31268316c34f361156029eff446c9c655b913da0952afa5edc921bd22898a886755bf')

    name = backend_name.split("_")[1].capitalize()

    qubits_csv_file = 'scripts/experimentos/dataframe_experiment' + name + '.csv'

    df_qubits = pd.read_csv(qubits_csv_file)
    ("Dataframe obtained")
    (df_qubits)

    for index, row in df_qubits.iterrows():

        T1 = row['T1']
        T2 = row['T2']
        probMeas0Prep1 = row['probMeas0Prep1']
        probMeas1Prep0 = row['probMeas1Prep0']
        qubit_error = row['readout_qubit_error']
        n_qubits = int(row['n_qubits'])
        depth = int(row['depth'])
        probability = float(row['probability'])

        circuit = generate_circuit(n_qubits, depth, probability)
        ("Circuit generated")

        dag = circuit_to_dag(circuit)

        op_nodes = dag.op_nodes()

        t_gates, phase_gates, h_gates, cnot_gates = count_gates(op_nodes)

        results_kullback = []
        results_jensen = []
        times = []

        for i in range(0, 5):
            fake_backend = service.get_backend(backend_name)

            circuit_copy = circuit.copy()

            start_time = time.time()

            kullback_qubit_error, jensen_qubit_error = calculate_configuration_qubit_error(circuit_copy,
                                                                                           fake_backend, T1,
                                                                                           T2,
                                                                                           probMeas0Prep1,
                                                                                           probMeas1Prep0,
                                                                                           qubit_error)

            end_time = time.time()

            execution_time = end_time - start_time

            results_kullback.append(kullback_qubit_error)
            results_jensen.append(jensen_qubit_error)
            times.append(execution_time)

        df_qubits.at[index, 't_gates'] = t_gates
        df_qubits.at[index, 'phase_gates'] = phase_gates
        df_qubits.at[index, 'h_gates'] = h_gates
        df_qubits.at[index, 'cnot_gates'] = cnot_gates
        df_qubits.at[index, 'kullback_error'] = sum(results_kullback) / len(results_kullback)
        df_qubits.at[index, 'jensen-error'] = sum(results_jensen) / len(results_jensen)
        df_qubits.at[index, 'time'] = sum(times) / len(times)

        df_qubits.to_csv(qubits_csv_file, index=False)
        (f"Row {index} saved")


execute_qubit_circuit("ibm_osaka")
