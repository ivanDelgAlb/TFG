from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, DCXGate, TGate, PhaseGate
import random
import math

def generar_circuito(n_qubits, profundidad):

    circuito = QuantumCircuit(n_qubits)

    array_qubits_1 = []
    array_qubits_2 = []

    # Se rellenan los arrays para ir usando las puertas
    for i in range(n_qubits):
        array_qubits_1.append(i)
        array_qubits_2.append(i)

    # Mientras no se haya alcanzado la profundidad deseada
    while circuito.depth() < profundidad:

        # Puerta de 1 qubit (probabilidad del 30%)
        if random.random() < 0.3:

            qubit_elegido = random.choice(array_qubits_1)
            array_qubits_1.remove(qubit_elegido)

            puerta = random.choice([TGate(), PhaseGate(theta=random.random() * 2 * math.pi), HGate()])
            circuito.append(puerta, [qubit_elegido])

            # Si el array está vacío se vuelve a empezar con todos
            if not array_qubits_1:
                for i in range(n_qubits):
                    array_qubits_1.append(i)

        # Puerta de 2 qubit      
        else:

            # Se elige el primer qubit
            qubit_elegido_1 = random.choice(array_qubits_2)
            array_qubits_2.remove(qubit_elegido_1)

            # Si no hay qubits en el array (numero inicial de qubits impar) se reinsertan
            if not array_qubits_2:
                for i in range(n_qubits):
                    array_qubits_2.append(i)

            qubit_elegido_2 = random.choice(array_qubits_2)
            while(qubit_elegido_2 == qubit_elegido_1):
                qubit_elegido_2 = random.choice(array_qubits_2)
            array_qubits_2.remove(qubit_elegido_2)

            # Puerta CNot
            circuito.append(DCXGate(), [qubit_elegido_1, qubit_elegido_2])
            
            if not array_qubits_2:
                for i in range(n_qubits):
                    array_qubits_2.append(i)

    return circuito