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
        'T1': 234,
        'T2': 213,
        'probMeas0Prep1': 1,
        'probMeas1Prep0': 2,
        'readout_qubit_error': 0.2,
        'n_qubits': 5,
        'depth': 5,
        't_gates': 12,
        'phase_gates': 11,
        'h_gates': 14,
        'cnot_gates': 13
     }
]

errors = predict_qubits_error(predictions, "ibm_kyoto")
print(errors)