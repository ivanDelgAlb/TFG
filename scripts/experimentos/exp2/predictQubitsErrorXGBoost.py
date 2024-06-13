import numpy as np
import xgboost as xgb


def predict(machine_name, data):
    """
    Predicts for the selected machine the error associated to the provided data
    :param machine_name: The name of the quantum machine
    :param data: The inputs for the model
    :type machine_name: str
    :type data: list of lists of lists
    :param depth: Depth value to filter the dataset
    :type depth: int
    :return: The predicted values
    :rtype: list of floats
    """

    formated_name = machine_name.split("_")[1].capitalize()

    models_directory = 'scripts/experimentos/exp2/xgboost_qubit_model_' + formated_name + '.model'
    file = models_directory

    xgb_model = xgb.Booster()
    xgb_model.load_model(file)

    data_np = np.array(data)

    if data_np.ndim == 1:
        data_np = data_np.reshape(1, -1)

    matrix_data = xgb.DMatrix(data_np)

    predictions = xgb_model.predict(matrix_data)

    return predictions

t1 = []
t2 = []
prob0 = []
prob1 = []
readout_error = []
n_qubits = []
t_gates = []
h_gates = []
phase_gates = []
cnot_gates = []


t1.append(234)
t2.append(123)
prob0.append(0.3)
prob1.append(0.1)
readout_error.append(2)
n_qubits.append(5)
t_gates.append(12)
h_gates.append(14)
phase_gates.append(15)
cnot_gates.append(11)

T1 = np.array(t1)
T2 = np.array(t2)
Prob0 = np.array(prob0)
Prob1 = np.array(prob1)
Error = np.array(readout_error)
n_qubits = np.array(n_qubits)
t_gates = np.array(t_gates)
h_gates = np.array(h_gates)
phase_gates = np.array(phase_gates)
cnot_gates = np.array(cnot_gates)

predictions = np.column_stack((T1, T2, Prob0, Prob1, Error, n_qubits, t_gates, h_gates, phase_gates, cnot_gates))

errors = predict("ibm_kyoto", predictions)

print(errors)