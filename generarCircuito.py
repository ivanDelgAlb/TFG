from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, DCXGate, TGate, PhaseGate
import random
import math
import unittest


def generate_circuit(n_qubits, depth):
    """
    Generates a quantum circuit given a specific number of qubits and a depth.

    :param n_qubits: Number of qubits for the circuit (it must be greater than 1).
    :param depth: Depth of the circuit (it must be positive).
    :type n_qubits: int
    :type depth: int
    :return: A quantum circuit from qiskit library.
    :rtype: QuantumCircuit
    """

    if n_qubits <= 1:
        raise ValueError("The circuit must have a positive number of qubits greater than 1")
    if depth <= 0:
        raise ValueError("The circuit must have a positive depth")

    circuit = QuantumCircuit(n_qubits)

    array_qubits_1 = []
    array_qubits_2 = []

    for i in range(n_qubits):
        array_qubits_1.append(i)
        array_qubits_2.append(i)

    while circuit.depth() < depth:

        if random.random() < 0.3:

            chosen_qubit = random.choice(array_qubits_1)
            array_qubits_1.remove(chosen_qubit)

            door = random.choice([TGate(), PhaseGate(theta=random.random() * 2 * math.pi), HGate()])
            circuit.append(door, [chosen_qubit])

            if not array_qubits_1:
                for i in range(n_qubits):
                    array_qubits_1.append(i)

        else:

            chosen_qubit_1 = random.choice(array_qubits_2)
            array_qubits_2.remove(chosen_qubit_1)

            if not array_qubits_2:
                for i in range(n_qubits):
                    array_qubits_2.append(i)

            chosen_qubit_2 = random.choice(array_qubits_2)
            while chosen_qubit_2 == chosen_qubit_1:
                chosen_qubit_2 = random.choice(array_qubits_2)
            array_qubits_2.remove(chosen_qubit_2)

            circuit.append(DCXGate(), [chosen_qubit_1, chosen_qubit_2])

            if not array_qubits_2:
                for i in range(n_qubits):
                    array_qubits_2.append(i)

    return circuit


class CircuitGenerationTests(unittest.TestCase):

    def test_negative_qubits_should_raise_exception(self):
        with self.assertRaises(ValueError):
            generate_circuit(0, 5)

    def test_negative_depth_should_raise_exception(self):
        with self.assertRaises(ValueError):
            generate_circuit(3, 0)

    def test_correct_depth(self):
        inputs = [
            (4, 2),
            (2, 3),
            (3, 4),
            (5, 2),
            (3, 5)
        ]
        expected_depths = [
            2,
            3,
            4,
            2,
            5
        ]

        for i, (n_qubits, depth) in enumerate(inputs):
            with self.subTest(n_qubits=n_qubits, depth=depth):
                actual_depth = generate_circuit(n_qubits, depth).depth()
                self.assertEqual(actual_depth, expected_depths[i])


if __name__ == '__main__':
    unittest.main()
