from datetime import datetime, timedelta
from keras.models import load_model
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def predict_qubits_error(predictions, machine_name, depth):
    try:
        machine_name = machine_name.split(" ")[1].capitalize()
        model = load_model('backend/models_perceptron/model_qubits_' + machine_name + '_' + depth +'.h5')
        normalized_data = normalized(predictions)  # Llama a la función normalized con la fecha
        errors = model.predict(normalized_data)
        errors = add_date_and_calibration(errors, predictions)
        return errors
    except FileNotFoundError:
        raise FileNotFoundError("The model is missing")
    
def add_date_and_calibration(errors, predictions):
    data_list = []

    date = datetime.now()

    for i, error in enumerate(errors):
        error_dict = {"Date": date.strftime("%Y-%m-%d %H:%M:%S")}
        date = date + timedelta(hours=2)
        print(error[0])
        error_dict['divergence'] = error[0]

        # Añadir las predicciones correspondientes
        if i < len(predictions):
            error_dict['T1'] = predictions[i].get('T1', None)
            error_dict['T2'] = predictions[i].get('T2', None)
            error_dict['Prob0'] = predictions[i].get('Prob0', None)
            error_dict['Prob1'] = predictions[i].get('Prob1', None)
            error_dict['Error'] = predictions[i].get('Error', None)

        data_list.append(error_dict)

    return data_list


def normalized(predictions):
    print(predictions)
    # Crear un DataFrame de Pandas
    df = pd.DataFrame(predictions)
    print(df)
    # Normalizar cada columna usando los valores mínimos y máximos de cada columna
    df_normalizado = df.apply(lambda fila: (fila - fila.min()) / (fila.max() - fila.min()), axis=1)
    print(df_normalizado)
    return df_normalizado
