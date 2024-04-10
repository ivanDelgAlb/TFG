from pymongo import MongoClient
import statistics

# Configuración de MongoDB Atlas (reemplaza con tus propios valores)
mongo_uri_Origen = "mongodb+srv://Marina:mongoTFG@tfg.qet3gme.mongodb.net/"
client_Origen = MongoClient(mongo_uri_Origen)

mongo_uri_Destino = "mongodb+srv://ivandelgadoalba:claveMongo@cluster0.pn3zcyq.mongodb.net/"
client_Destino = MongoClient(mongo_uri_Destino)

# Nombre de la colección en MongoDB Compass
collection_name_Destino = "derivado"
collection_name_Origen = "data"

# Conectarse a la base de datos en MongoDB Atlas
db_Origen = client_Origen["TFG"]
db_Destino = client_Destino["TFG"]

db_Destino[collection_name_Destino].drop()
print("Colección borrada con éxito")

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

    
datos = db_Origen[collection_name_Origen].find()

for dato in datos:

    qubits = dato['properties']['qubits']
    qubits_derivados = []

    gates = dato["properties"]["gates"]
    gates_derivados = []
        
    atributos = ["T1", "T2", "prob_meas0_prep1", "prob_meas1_prep0", "readout_error","gate_error", "gate_length"] 
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

    dato['properties'].pop('general', None)
    dato['properties'].pop('general_qlists', None)
    dato.pop('configuration', None)


    collection = db_Destino[collection_name_Destino]
    collection.insert_one(dato)

   
        
print("Se insertado todos los valores derivados correctamente")
