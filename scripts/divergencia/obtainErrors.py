from calculateNoiseError import calculate_configuration_qubit_error, calculate_configuration_gate_error
from generateCircuit import generate_circuit
from qiskit_ibm_runtime import QiskitRuntimeService
import pandas as pd
import random
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
                                   token='8744729d1df2b54f6d544d5e4d49e3c1929372023734570e3db2f4a5568cf68ce8140213570c3a79c13548a13a0106bd3cd23c16578ef36b8e0139407b93d67a')
    name = backend_name.split("_")[1].capitalize()
    
    qubits_csv_file = 'dataframe_perceptron_qubits_' + name + '.csv'

    df_qubits = pd.read_csv(qubits_csv_file)
    print("Dataframe obtained")

    for index, row in df_qubits.iterrows():
        
        fake_backend = service.get_backend(backend_name)
        T1 = row['T1']
        T2 = row['T2']
        probMeas0Prep1 = row['probMeas0Prep1']
        probMeas1Prep0 = row['probMeas1Prep0']
        qubit_error = row['readout_qubit_error']
        n_qubits = int(row['n_qubits'])
        depth = int(row['depth'])

        circuit = generate_circuit(n_qubits, depth)
        print("Circuit generated")

        dag = circuit_to_dag(circuit)

        op_nodes = dag.op_nodes()

        t_gates, phase_gates, h_gates, cnot_gates = count_gates(op_nodes)

        kullback_qubit_error, jensen_qubit_error = calculate_configuration_qubit_error(circuit,
                                                                                       fake_backend, T1,
                                                                                       T2,
                                                                                       probMeas0Prep1,
                                                                                       probMeas1Prep0,
                                                                                       qubit_error)

        df_qubits.at[index, 't_gates'] = t_gates
        df_qubits.at[index, 'phase_gates'] = phase_gates
        df_qubits.at[index, 'h_gates'] = h_gates
        df_qubits.at[index, 'cnot_gates'] = cnot_gates
        df_qubits.at[index, 'kullback_error'] = kullback_qubit_error
        df_qubits.at[index, 'jensen-error'] = jensen_qubit_error

        df_qubits.to_csv(qubits_csv_file, index=False)
        print(f"Row {index} saved")


def execute_gate_circuit(backend_name):
    service = QiskitRuntimeService(channel='ibm_quantum',
                                   token='8744729d1df2b54f6d544d5e4d49e3c1929372023734570e3db2f4a5568cf68ce8140213570c3a79c13548a13a0106bd3cd23c16578ef36b8e0139407b93d67a')
    name = backend_name.split("_")[1].capitalize()
    
    gates_csv_file = 'dataframe_perceptron_gates_' + name + '.csv'

    df_gates = pd.read_csv(gates_csv_file)
    print("Dataframe obtained")

    qubits = [5, 10, 15]
    depths = [5, 10, 15]

    for index, row in df_gates.iterrows():

        n_qubits = random.choice(qubits)
        depth = random.choice(depths)

        circuit = generate_circuit(n_qubits, depth)
        print("Circuit generated")

        dag = circuit_to_dag(circuit)

        op_nodes = dag.op_nodes()

        t_gates, phase_gates, h_gates, cnot_gates = count_gates(op_nodes)

        one_qubit_error = row['gate_error_one_qubit']
        two_qubit_error = row['gate_error_two_qubit']

        fake_backend = service.get_backend(backend_name)

        kullback_gate_error, jensen_gate_error = calculate_configuration_gate_error(circuit,
                                                                                    fake_backend,
                                                                                    one_qubit_error,
                                                                                    two_qubit_error)
        
        df_gates.at[index, 'n_qubits'] = n_qubits
        df_gates.at[index, 't_gates'] = t_gates
        df_gates.at[index, 'phase_gates'] = phase_gates
        df_gates.at[index, 'h_gates'] = h_gates
        df_gates.at[index, 'cnot_gates'] = cnot_gates
        df_gates.at[index, 'kullback_error'] = kullback_gate_error
        df_gates.at[index, 'jensen-error'] = jensen_gate_error

        df_gates.to_csv(gates_csv_file, index=False)
        print(f"Row {index} saved")


