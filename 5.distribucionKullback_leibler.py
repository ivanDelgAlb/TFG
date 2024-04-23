from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit import transpile
from qiskit_aer.noise import NoiseModel
from generarCircuito import generate_circuit
from qiskit_aer import AerSimulator
from math import log
from qiskit.providers.models.backendproperties import BackendProperties
from qiskit.providers import Backend


def generate_backend_configuration(T1, T2, prob_meas0_prep1, prob_meas1_prep0, readout_error, date, backend):
    new_values = {
        'T1': T1,
        'T2': T2,
        'prob_meas0_prep1': prob_meas0_prep1,
        'prob_meas1_prep0': prob_meas1_prep0,
        'readout_error': readout_error
    }

    configuration = backend.configuration()
    properties = backend.properties()
    qubits = properties.to_dict()['qubits']
    gates = properties.to_dict()['gates']
    general = properties.to_dict()['general']

    new_qubits = []
    for list in qubits:
        new_qubit_data = []
        for dictionary in list:
            if dictionary['name'] in new_values:
                dictionary['value'] = new_values[dictionary['name']]
            new_qubit_data.append(dictionary)
        new_qubits.append(new_qubit_data)

    new_data = {
        'backend_name': backend.name,
        'backend_version': properties.backend_version,
        'last_update_date': date,
        'qubits': new_qubits,
        'gates': gates,
        'general': general
    }
    new_properties = BackendProperties.from_dict(new_data)

    new_backend = backend
    new_backend.configuration = configuration
    new_backend.properties = new_properties

    return new_backend


def calculate_configuration_error(circuit, backend):
    """
    Calculates the Kullback-Leibler divergence given a quantum circuit and a configuration for the quantum machine in comparison to an ideal machine
    :param circuit: Quantum circuit from qiskit
    :param configuration: Configuration from a quantum machine
    :type circuit: QuantumCircuit
    :return: The Kullback-Leibler divergence
    :rtype: float
    """
    circuit.measure_all()

    shots = 1000

    noise_model = NoiseModel.from_backend(backend)

    transpiled_circuit = transpile(circuit, backend=backend)
    real_backend = generate_backend_configuration(225.34260521453552, 145.04435990153732, 0.023973228346456682, 0.024713385826771656, 0.024343307086614172, '2024-02-27T19:38:28', backend)
    real_machine = AerSimulator.from_backend(real_backend)
    job_real_machine = real_machine.run(transpiled_circuit, shots=shots)
    counts_real_machine = job_real_machine.result().get_counts(0)

    probabilities_real_machine = {state: counts_real_machine[state] / shots for state in counts_real_machine}
    print("Backend with noise executed")

    # ----------------------------------------------------------------------------------------

    noise_model.reset()
    ideal_machine = AerSimulator.from_backend(real_backend)

    job_ideal_machine = ideal_machine.run(transpiled_circuit, shots=shots)
    counts_ideal_machine = job_ideal_machine.result().get_counts()

    probabilities_ideal_machine = {state: counts_ideal_machine[state] / shots for state in counts_ideal_machine}
    print("Ideal backend executed")

    divergence = 0.0
    for status in probabilities_real_machine:
        if probabilities_ideal_machine.get(status, 0) != 0:
            divergence += probabilities_ideal_machine.get(status, 0) * log(
                (probabilities_ideal_machine.get(status, 0) / probabilities_real_machine[status]))
    print("Divergence calculated")

    return divergence


service = QiskitRuntimeService(channel='ibm_quantum',
                                   token='8744729d1df2b54f6d544d5e4d49e3c1929372023734570e3db2f4a5568cf68ce8140213570c3a79c13548a13a0106bd3cd23c16578ef36b8e0139407b93d67a')
fake_backend = service.get_backend('ibm_brisbane')
circuit = generate_circuit(4, 5)
print(calculate_configuration_error(circuit, fake_backend))
