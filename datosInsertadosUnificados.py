import requests
from pymongo import MongoClient
import statistics

# Configuración de MongoDB Atlas (reemplaza con tus propios valores)
mongo_uri = "mongodb+srv://Marina:mongoTFG@tfg.qet3gme.mongodb.net/"
client = MongoClient(mongo_uri)

# Ruta al directorio que contiene los archivos JSON en el repositorio de GitHub
github_repo_url = "https://github.com/Zakaria-Dahi/TFG_UMA_2023_2204"
data_directory = "data"

# Nombre de la colección en MongoDB Compass
collection_name_data = "data"
collection_name_procesado = "procesado"
collection_name_derivado = "derivado"


github_username = "marinasayago"
github_token = "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"

# Conectarse a la base de datos en MongoDB Atlas
db = client["TFG"]

# Borro las colecciones por si tenían algún dato
db[collection_name_data].drop()
print("Colección data borrada con éxito")
db[collection_name_procesado].drop()
print("Colección procesado borrada con éxito")
db[collection_name_derivado].drop()
print("Colección derivado borrada con éxito")


# Autenticación con la API de GitHub
auth_url = "https://api.github.com/user"
auth_response = requests.get(auth_url, auth=(github_username, github_token))
auth_response.raise_for_status()
print("Autenticación exitosa")

# Obtener la lista de archivos JSON en la carpeta del repositorio de GitHub
repo_contents_url = f"https://api.github.com/repos/Zakaria-Dahi/TFG_UMA_2023_2204/contents/{data_directory}"
contents_response = requests.get(repo_contents_url, auth=(github_username, github_token))
contents_response.raise_for_status()

# Obtener nombres de archivos JSON
files = [file["name"] for file in contents_response.json() if file["name"].endswith(".json")]

# Iterar sobre los archivos y cargar los datos en MongoDB
for file in files:

    try:
        # Modifica la URL para apuntar a la versión RAW del archivo en GitHub
        raw_url = f"https://raw.githubusercontent.com/Zakaria-Dahi/TFG_UMA_2023_2204/main/data/{file}"

        response = requests.get(raw_url, auth=(github_username, github_token))
        response.raise_for_status()  # Verificar si hay errores en la respuesta HTTP
        json_data = response.json()
        
        # Insertar datos en la colección de MongoDB Compass
        collection = db[collection_name_data]
        collection.insert_many(json_data)
        print(f"Datos insertados con éxito para el archivo: {file}")

    except Exception as e:
        print(f"Error: {e}")



print("Proceso completado.")


# SELECCIÓN DE DATOS
print("Empieza la selección de datos")
datos = db[collection_name_data].find()

for dato in datos:
    # Eliminar atributos no deseados
    qubits = dato['properties']['qubits']

    qubits_sin_atributos = []

    for qubit in qubits:
        qubits_sin_atributo = []  # Inicializa una lista vacía para cada qubit
        for q in qubit:
            if q['name'] != 'frequency' and q['name'] != 'anharmonicity':
                qubits_sin_atributo.append(q)  # Agrega el qubit a la lista si cumple con las condiciones
        qubits_sin_atributos.append(qubits_sin_atributo)


    # Crear una nueva lista de qubits sin los que tienen nombre 'frequency'

    
    # Asignar la lista de qubits sin 'frequency' de vuelta a la propiedad 'qubits' del dato
    dato['properties']['qubits'] = qubits_sin_atributos
    
    
    # Eliminar otros atributos no deseados
    dato['properties'].pop('general', None)
    dato['properties'].pop('general_qlists', None)
    dato.pop('configuration', None)
    
    # Insertar documento modificado en la colección de destino
    collection = db[collection_name_procesado]
    collection.insert_one(dato)

print("Se han seleccionado los datos correctamente")



# CALCULO DE LOS VALORES DERIVADOS

print("Empieza el cálculo de datos derivados")
def calcMedia(datos, nqubit, atributo):
    media = 0
    cont = 0

    for dato in datos:
        if nqubit > 0:
            if len(dato['qubits']) == nqubit:
                for gate in dato['parameters']:
                    media += gate['value']
                    cont += 1
        else:
            for qubit in dato:
                if qubit['name'] == atributo:
                    media += qubit['value']
                    cont += 1

    if cont > 0:
        media = media / cont
    
    return media


def calcMediana(datos, nqubit, atributo):
    valores = []

    for dato in datos:
        if nqubit > 0:
            if len(dato['qubits']) == nqubit:
                for gate in dato['parameters']:
                    if gate['name'] == atributo:
                        valores.append(gate['value'])
        else:
            for qubit in dato:
                if qubit['name'] == atributo:
                    valores.append(qubit['value'])  # Agrega el qubit a la lista si cumple con las condiciones

    n = len(valores)
    
    if n % 2 == 0:
        # Si el número de datos es par
        mediana = (valores[n//2 - 1] + valores[n//2]) / 2
    else:
        # Si el número de datos es impar
        mediana = valores[n//2]

    return mediana


def calcDesviacion(datos, nqubit, atributo):
    valores = []

    for dato in datos:
        if nqubit > 0:
            if len(dato['qubits']) == nqubit:
                for gate in dato['parameters']:
                    if gate["name"] == atributo:
                        valores.append(gate['value'])
        else:
            for qubit in dato:
                if qubit["name"] == atributo:
                    valores.append(qubit['value'])

    if len(valores) < 2:
        return None  # None si no hay suficientes datos

    desviacion_estandar = statistics.stdev(valores)
    return desviacion_estandar

    
datos = db[collection_name_procesado].find()

for dato in datos:

    qubits = dato['properties']['qubits']
    qubits_derivados = []

    gates = dato["properties"]["gates"]
    gates_derivados = []
        
    atributos = ["T1", "T2", "prob_meas0_prep1", "prob_meas1_prep0", "readout_length","gate_error", "gate_length"] 
    nqubits = [1, 2]

    for atributo in atributos:

        if atributo != "gate_error" and atributo != "gate_length":

            documento = {
                "name": atributo,
                "media": calcMedia(qubits, -1, atributo),
                "mediana": calcMediana(qubits, -1, atributo),
                "desviacion": calcDesviacion(qubits, -1, atributo)
            }

            qubits_derivados.append(documento)
        
        else:

            for nqubit in nqubits:
                documento = {
                    "name": atributo,
                    "nºqubits": nqubit,
                    "media": calcMedia(gates, nqubit, atributo),
                    "mediana": calcMediana(gates, nqubit, atributo),
                    "desviacion": calcDesviacion(gates, nqubit, atributo)
                }
                gates_derivados.append(documento)


    dato['properties']['qubits'] = qubits_derivados
    dato['properties']['gates'] = gates_derivados


    collection = db[collection_name_derivado]
    collection.insert_one(dato)

   
        
print("Se insertado todos los valores derivados correctamente")
