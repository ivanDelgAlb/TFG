from qiskit import transpile
from qiskit_aer.noise import NoiseModel
from qiskit_aer import AerSimulator
from math import log
from qiskit.providers.models.backendproperties import BackendProperties


def generate_qubit_backend_configuration(T1, T2, prob_meas0_prep1, prob_meas1_prep0, readout_error_qubits, backend):
    """
    Generates a BackendV2 object with the given configuration for the qubits
    :param backend: A backend from, the QiskitService library
    :param T1: median of T1 of the qubits
    :param T2: median of T2 of the qubits
    :param prob_meas0_prep1: median of prob_meas0_prep1 of the qubits
    :param prob_meas1_prep0: median of prob_meas1_prep0 of the qubits
    :param readout_error_qubits: median of readout_error of the qubits
    :type backend: BackendV2
    :type T1: float
    :type T2: float
    :type prob_meas0_prep1: float
    :type prob_meas1_prep0: float
    :type readout_error_qubits: float
    :return: A backend with the given configuration
    :rtype: BackendV2
    """

    new_values = {
        'T1': T1,
        'T2': T2,
        'prob_meas0_prep1': prob_meas0_prep1,
        'prob_meas1_prep0': prob_meas1_prep0,
        'readout_error': readout_error_qubits
    }

    fake_date = '2024-02-27T19:38:28'
    configuration = backend.configuration()
    properties = backend.properties()
    qubits = properties.to_dict()['qubits']
    gates = properties.to_dict()['gates']
    general = properties.to_dict()['general']

    new_qubits = []
    for qubit in qubits:
        new_qubit_data = []
        for dictionary in qubit:
            if dictionary['name'] in new_values:
                dictionary['value'] = new_values[dictionary['name']]
            new_qubit_data.append(dictionary)
        new_qubits.append(new_qubit_data)

    new_data = {
        'backend_name': backend.name,
        'backend_version': properties.backend_version,
        'last_update_date': fake_date,
        'qubits': new_qubits,
        'gates': gates,
        'general': general
    }
    new_properties = BackendProperties.from_dict(new_data)

    new_backend = backend
    new_backend.configuration = configuration
    new_backend.properties = new_properties

    return new_backend


def generate_gate_backend_configuration(error_one_qubit_gates, error_two_qubit_gates, backend):
    """
    Generates a BackendV2 object with the given configuration for the gates
    :param backend: A backend from, the QiskitService library
    :param error_one_qubit_gates: median of the gate_error of 1-qubit-entrance gate
    :param error_two_qubit_gates: median of the gate_error of 2-qubits-entrance gate
    :type backend: BackendV2
    :type error_one_qubit_gates: float
    :type error_two_qubit_gates: float
    :return: A backend with the given configuration
    :rtype: BackendV2
    """

    fake_date = '2024-02-27T19:38:28'
    configuration = backend.configuration()
    properties = backend.properties()
    qubits = properties.to_dict()['qubits']
    gates = properties.to_dict()['gates']
    general = properties.to_dict()['general']

    new_gates = []
    for gate in gates:
        if len(gate['qubits']) == 1:
            for parameter in gate['parameters']:
                if parameter['name'] == 'gate_error':
                    parameter['value'] = error_one_qubit_gates
        else:
            for parameter in gate['parameters']:
                if parameter['name'] == 'gate_error':
                    parameter['value'] = error_two_qubit_gates
        new_gates.append(gate)

    new_data = {
        'backend_name': backend.name,
        'backend_version': properties.backend_version,
        'last_update_date': fake_date,
        'qubits': qubits,
        'gates': new_gates,
        'general': general
    }
    new_properties = BackendProperties.from_dict(new_data)

    new_backend = backend
    new_backend.configuration = configuration
    new_backend.properties = new_properties

    return new_backend


def calculate_configuration_qubit_error(circuit, backend, T1, T2, prob_meas0_prep1, prob_meas1_prep0,
                                        readout_error_qubits):
    """
    Calculates the Kullback-Leibler divergence given a quantum circuit and a configuration for the quantum machine in comparison to an ideal machine
    :param circuit: Quantum circuit from qiskit
    :param backend: A backend from, the QiskitService library
    :param T1: median of T1 of the qubits
    :param T2: median of T2 of the qubits
    :param prob_meas0_prep1: median of prob_meas0_prep1 of the qubits
    :param prob_meas1_prep0: median of prob_meas1_prep0 of the qubits
    :param readout_error_qubits: median of readout_error of the qubits
    :type circuit: QuantumCircuit
    :type backend: BackendV2
    :type T1: float
    :type T2: float
    :type prob_meas0_prep1: float
    :type prob_meas1_prep0: float
    :type readout_error_qubits: float
    :return: A tuple that contains the Kullback-Leibler divergence and the Jensen-Shannon divergence
    :rtype: tuple(float, float)
    """
    ("Calculating qubit configuration error")
    circuit.measure_all()

    shots = 1000

    noise_model = NoiseModel.from_backend(backend)

    transpiled_circuit = transpile(circuit, backend=backend)
    real_backend = generate_qubit_backend_configuration(T1, T2, prob_meas0_prep1, prob_meas1_prep0,
                                                        readout_error_qubits, backend)
    real_machine = AerSimulator.from_backend(real_backend)
    job_real_machine = real_machine.run(transpiled_circuit, shots=shots)
    counts_real_machine = job_real_machine.result().get_counts(0)

    probabilities_real_machine = {state: counts_real_machine[state] / shots for state in counts_real_machine}
    ("Backend with noise executed")

    # ----------------------------------------------------------------------------------------

    noise_model.reset()
    ideal_machine = AerSimulator.from_backend(real_backend)

    job_ideal_machine = ideal_machine.run(transpiled_circuit, shots=shots)
    counts_ideal_machine = job_ideal_machine.result().get_counts()

    probabilities_ideal_machine = {state: counts_ideal_machine[state] / shots for state in counts_ideal_machine}
    ("Ideal backend executed")

    kullback_divergence = calculate_kullback_divergence(probabilities_real_machine, probabilities_ideal_machine)
    ("Kullback-Leibler divergence calculated")

    jensen_divergence = calculate_jensen_divergence(probabilities_real_machine, probabilities_ideal_machine)
    ("Jensen-Shannon divergence calculated")

    return kullback_divergence, jensen_divergence


def calculate_configuration_gate_error(circuit, backend, error_one_qubit_gates, error_two_qubit_gates):
    """
    Calculates the Kullback-Leibler divergence given a quantum circuit and a configuration for the quantum machine in comparison to an ideal machine
    :param circuit: Quantum circuit from qiskit
    :param backend: A backend from, the QiskitService library
    :param error_one_qubit_gates: median of readout_error of the gates using one qubit
    :param error_two_qubit_gates: median of readout_error of the gates using two qubits
    :type circuit: QuantumCircuit
    :type backend: BackendV2
    :type error_one_qubit_gates: float
    :type error_two_qubit_gates: float
    :return: A tuple that contains the Kullback-Leibler divergence and the Jensen-Shannon divergence
    :rtype: tuple(float, float)
    """
    ("Calculating gate configuration error")
    circuit.measure_all()

    shots = 1000

    noise_model = NoiseModel.from_backend(backend)

    transpiled_circuit = transpile(circuit, backend=backend)
    real_backend = generate_gate_backend_configuration(error_one_qubit_gates, error_two_qubit_gates, backend)
    real_machine = AerSimulator.from_backend(real_backend)
    job_real_machine = real_machine.run(transpiled_circuit, shots=shots)
    counts_real_machine = job_real_machine.result().get_counts(0)

    probabilities_real_machine = {state: counts_real_machine[state] / shots for state in counts_real_machine}
    ("Backend with noise executed")

    # ----------------------------------------------------------------------------------------

    noise_model.reset()
    ideal_machine = AerSimulator.from_backend(real_backend)

    job_ideal_machine = ideal_machine.run(transpiled_circuit, shots=shots)
    counts_ideal_machine = job_ideal_machine.result().get_counts()

    probabilities_ideal_machine = {state: counts_ideal_machine[state] / shots for state in counts_ideal_machine}
    ("Ideal backend executed")

    kullback_divergence = calculate_kullback_divergence(probabilities_real_machine, probabilities_ideal_machine)
    ("Kullback-Leibler divergence calculated")

    jensen_divergence = calculate_jensen_divergence(probabilities_real_machine, probabilities_ideal_machine)
    ("Jensen-Shannon divergence calculated")

    return kullback_divergence, jensen_divergence


def calculate_kullback_divergence(probabilities_ideal_machine, probabilities_real_machine):
    """
    Calculates the Kullback-Leibler divergence given two dictionaries with the results of an execution of a circuit and their probabilities
    :param probabilities_real_machine: Dictionary of the execution of a circuit and their probabilities of a real quantum machine
    :param probabilities_ideal_machine: Dictionary of the execution of a circuit and their probabilities of an ideal quantum machine
    :type probabilities_ideal_machine: dict[str, float]
    :type probabilities_real_machine: dict[str, float]
    :return: The Kullback-Leibler divergence of the distributions
    :rtype: float
    """
    divergence = 0.0
    for status in probabilities_real_machine:
        if probabilities_ideal_machine.get(status, 0) != 0:
            divergence += probabilities_ideal_machine.get(status, 0) * log(
                (probabilities_ideal_machine.get(status, 0) / probabilities_real_machine[status]))

    return divergence


def calculate_jensen_divergence(probabilities_real_machine, probabilities_ideal_machine):
    """
    Calculates the Jensen-Shannon divergence given two dictionaries with the results of an execution of a circuit and their probabilities
    :param probabilities_real_machine: Dictionary of the execution of a circuit and their probabilities of a real quantum machine
    :param probabilities_ideal_machine: Dictionary of the execution of a circuit and their probabilities of an ideal quantum machine
    :type probabilities_ideal_machine: dict[str, float]
    :type probabilities_real_machine: dict[str, float]
    :return: The Jensen-Shannon divergence of the distributions
    :rtype: float
    """

    mixture_distribution = {}
    
    for status in set(probabilities_real_machine.keys()).union(set(probabilities_ideal_machine.keys())):
        prob_real = probabilities_real_machine.get(status, 0)
        prob_ideal = probabilities_ideal_machine.get(status, 0)
        mixture_distribution[status] = 0.5 * prob_real + 0.5 * prob_ideal
    
    divergence = 0.5 * calculate_kullback_divergence(probabilities_ideal_machine, mixture_distribution) + \
                 0.5 * calculate_kullback_divergence(probabilities_real_machine, mixture_distribution)
    
    return divergence


'''
circuit = generate_circuit(25, 5)
("Circuit generated")

service = QiskitRuntimeService(channel='ibm_quantum',
                                   token='8744729d1df2b54f6d544d5e4d49e3c1929372023734570e3db2f4a5568cf68ce8140213570c3a79c13548a13a0106bd3cd23c16578ef36b8e0139407b93d67a')

fake_backend_brisbane = service.get_backend('ibm_brisbane')
fake_date = '2024-02-27T19:38:28'
qubit_kullback_error, qubit_jensen_error = calculate_configuration_qubit_error(circuit, fake_backend_brisbane, 225.34260521453552, 145.04435990153732, 0.023973228346456682, 0.024713385826771656, 0.024343307086614172)
("Kullback error on qubits: " + str(qubit_kullback_error))
("Jensen error on qubits: " + str(qubit_jensen_error))

fake_backend_brisbane = service.get_backend('ibm_brisbane')
gate_kullback_error, gate_jensen_error = calculate_configuration_gate_error(circuit, fake_backend_brisbane, 0.0000785365131764739, 0.007890508160354082)
("Kullback error on gates: " + str(gate_kullback_error))
("Jensen error on gates: " + str(gate_jensen_error))
'''
