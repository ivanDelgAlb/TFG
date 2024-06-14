from keras.models import load_model
import pandas as pd

def predict_qubits_error(predictions, machine_name):
    try:
        machine_name = machine_name.split("_")[1].capitalize()

        models_directory = 'scripts/experimentos/exp2/model_qubits_' + machine_name + '.h5'

        model = load_model(models_directory) 
        normalized_data = pd.DataFrame(predictions)

        columns_to_normalize = ['T1','T2','probMeas0Prep1','probMeas1Prep0','readout_qubit_error']

        normalized_df = normalized_data[columns_to_normalize].apply(lambda row: (row - row.min()) / (row.max() - row.min()), axis=1)

        normalized_data[['T1','T2','probMeas0Prep1','probMeas1Prep0','readout_qubit_error']] = normalized_df
            
        errors = model.predict(normalized_data)

        return errors
    except FileNotFoundError:
        raise FileNotFoundError("The model is missing")
    

predictions = [
    {
        'T1': 220.5563820634488,
        'T2': 96.8492816613982,
        'probMeas0Prep1': 0.0146,
        'probMeas1Prep0': 0.0162,
        'readout_qubit_error': 0.0153999999999999,
        'n_qubits': 10,
        'depth': 10,
        't_gates': 22,
        'phase_gates': 15,
        'h_gates': 15,
        'cnot_gates': 16
     }
]

errors = predict_qubits_error(predictions, "ibm_kyoto")
print(errors)