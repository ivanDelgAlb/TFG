from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, DCXGate, TGate, PhaseGate
from qiskit.converters import circuit_to_dag
from qiskit.visualization import dag_drawer
import random
import math

def generar_circuito(n_qubits, puertas_1_qubit, puertas_2_qubit):

    total_puertas = puertas_1_qubit + puertas_2_qubit
    circuito = QuantumCircuit(n_qubits)

    array_qubits_1 = []
    array_qubits_2 = []

    for i in range(n_qubits):
        array_qubits_1.append(i)
        array_qubits_2.append(i)

    while total_puertas > 0:
        if random.randint(1, total_puertas) <= puertas_1_qubit:

            qubit_elegido = random.choice(array_qubits_1)
            array_qubits_1.remove(qubit_elegido)

            puerta = random.randint(1, 3)

            if puerta == 1:
                # Puerta de T
                circuito.append(TGate(), [qubit_elegido])
            elif puerta == 2:
                # Puerta de fase
                theta = random.random() * 2 * math.pi
                circuito.append(PhaseGate(theta=theta), [qubit_elegido])
            else: 
                # Puerta Hadamard
                circuito.append(HGate(), [qubit_elegido])
            
            puertas_1_qubit -= 1

            if not array_qubits_1:
                for i in range(n_qubits):
                    array_qubits_1.append(i)
            
        else:

            qubit_elegido_1 = random.choice(array_qubits_2)
            array_qubits_2.remove(qubit_elegido_1)
            qubit_elegido_2 = random.choice(array_qubits_2)
            array_qubits_2.remove(qubit_elegido_2)

            circuito.append(DCXGate(), [qubit_elegido_1, qubit_elegido_2])
            
            if not array_qubits_2:
                for i in range(n_qubits):
                    array_qubits_2.append(i)

        total_puertas -= 1

    return circuito

'''
circuito = generar_circuito(4, 3, 5)
circuito.draw(output='mpl', filename='circuit.png')


    dag = circuit_to_dag(circuito)
    print(dag.depth())
'''