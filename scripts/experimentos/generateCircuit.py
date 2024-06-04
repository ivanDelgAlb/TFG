from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, DCXGate, TGate, PhaseGate
import random
import math
import unittest


def generate_circuit(n_qubits, depth, probability_one_qubit_gate):
    """
    Generates a quantum circuit given a specific number of qubits and a depth.

    :param n_qubits: Number of qubits for the circuit (it must be greater than 1).
    :param depth: Depth of the circuit (it must be positive).
    :param probability_one_qubit_gate probability to generate gates with one qubit input (between 0 and 1).
    :type n_qubits: int
    :type depth: int
    :type probability_one_qubit_gate: float
    :return: A quantum circuit from qiskit library.
    :rtype: QuantumCircuit
    """

    if n_qubits <= 1:
        raise ValueError("The circuit must have a positive number of qubits greater than 1")
    if depth <= 0:
        raise ValueError("The circuit must have a positive depth")
    if probability_one_qubit_gate < 0 or 1 < probability_one_qubit_gate:
        raise ValueError("The probability must be between 0 and 1")

    circuit = QuantumCircuit(n_qubits)

    array_qubits_1 = []
    array_qubits_2 = []

    for i in range(n_qubits):
        array_qubits_1.append(i)
        array_qubits_2.append(i)

    while circuit.depth() < depth:

        if random.random() < probability_one_qubit_gate:

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
            generate_circuit(0, 5, 0.3)

    def test_negative_depth_should_raise_exception(self):
        with self.assertRaises(ValueError):
            generate_circuit(3, 0, 0.3)

    def test_negative_probability_should_raise_exception(self):
        with self.assertRaises(ValueError):
            generate_circuit(5, 5, -1)
            
    def test_probability_greater_than_zero_should_raise_exception(self):
        with self.assertRaises(ValueError):
            generate_circuit(5, 5, 5)

    def test_correct_depth(self):
        inputs = [
            (4, 2, 0.3),
            (2, 3, 0.5),
            (3, 4, 0.4),
            (5, 2, 0.2),
            (3, 5, 0.3),
            (20, 5, 0.3)
        ]
        expected_depths = [
            2,
            3,
            4,
            2,
            5,
            5
        ]

        for i, (n_qubits, depth, probability) in enumerate(inputs):
            with self.subTest(n_qubits=n_qubits, depth=depth, probability=probability):
                actual_depth = generate_circuit(n_qubits, depth, probability).depth()
                self.assertEqual(actual_depth, expected_depths[i])


if __name__ == '__main__':
    unittest.main()
