import numpy as np
import joblib
from datetime import datetime, timedelta
import gc
import os

def predict(machine_name, data, depth):
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
    print(data)
    print("---------------------------")
    formated_name = machine_name.split(" ")[1].capitalize()
    file = f'backend/models_xgboost_qubits/xgboost_qubit_model_{formated_name}_{depth}.joblib'

    if not os.path.exists(file):
        raise FileNotFoundError(f"Model file {file} not found")

    try:
        # Liberar memoria antes de cargar el modelo
        gc.collect()
        final_model = joblib.load(file)
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None

    # Convertir data a un array numpy y ajustar las dimensiones
    data_np = np.array(data).reshape(len(data), -1)

    try:
        # Dividir los datos en partes más pequeñas si es necesario
        chunk_size = 1000  # Ajusta el tamaño del chunk según la memoria disponible
        predictions = []
        for i in range(0, len(data_np), chunk_size):
            chunk_data = data_np[i:i + chunk_size]
            chunk_predictions = final_model.predict(chunk_data)
            predictions.extend(chunk_predictions)
    except Exception as e:
        print(f"Error making predictions: {e}")
        return None
    
    

    predictions = add_date_and_calibration(predictions, data)

    return predictions

def add_date_and_calibration(errors, predictions):
    data_list = []
    date = datetime.now()

    for i, error in enumerate(errors):
        error_dict = {"Date": date.strftime("%Y-%m-%d %H:%M:%S")}
        date += timedelta(hours=2)
        error_dict['divergence'] = error

        print(errors)

        # Añadir las predicciones correspondientes
        if i < len(predictions):
            error_dict['t1'] = predictions[i][0]
            error_dict['t2'] = predictions[i][1]
            error_dict['prob0'] = predictions[i][2]
            error_dict['prob1'] = predictions[i][3]
            error_dict['error'] = predictions[i][4]

        data_list.append(error_dict)

    return data_list