from math import log
from generarCircuito import generar_circuito
from qiskit import transpile
from qiskit_aer import AerSimulator

circuito = generar_circuito(4, 5)
circuito.measure_all()

shots = 1000

simulator = AerSimulator()

transpiled_circuit = transpile(circuito, simulator)

sim_automatic = AerSimulator(method='automatic')
job_automatic = sim_automatic.run(transpiled_circuit, shots=shots)
counts_automatic = job_automatic.result().get_counts(0)

probabilities_simulator = {state: counts_automatic[state] / shots for state in counts_automatic}

from qiskit.providers.models import BackendConfiguration
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(channel='ibm_quantum',token='8744729d1df2b54f6d544d5e4d49e3c1929372023734570e3db2f4a5568cf68ce8140213570c3a79c13548a13a0106bd3cd23c16578ef36b8e0139407b93d67a')
backend = service.get_backend('ibm_brisbane')
real_machine = AerSimulator.from_backend(backend)

job_real_machine = real_machine.run(transpiled_circuit, shots=shots)
counts_real_machine = job_real_machine.result().get_counts(0)

probabilities_real_machine = {state: counts_real_machine[state] / shots for state in counts_real_machine}

print("Probabilidades simulador: ", probabilities_simulator)
print("Probabilidades maquina real: ", probabilities_real_machine)

distribution = 0.0
for status in probabilities_real_machine:
    if(probabilities_simulator.get(status, 0) != 0):
        distribution += probabilities_simulator.get(status, 0) * log((probabilities_simulator.get(status, 0) / probabilities_real_machine[status]))

print(distribution)