import requests
from pymongo import MongoClient

def descargar_ficheros():


    url = "https://github.com/Zakaria-Dahi/TFG_UMA_2023_2204"
    username = "IvanUma"
    token = "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"

    auth_url = "https://api.github.com/user"
    auth_response = requests.get(auth_url, auth=(username, token))
    auth_response.raise_for_status()

    repo_contents_url = f"https://api.github.com/repos/Zakaria-Dahi/TFG_UMA_2023_2204/contents/data"
    contents_response = requests.get(repo_contents_url, auth=(username, token))
    contents_response.raise_for_status()

    archivos = [archivo["name"] for archivo in contents_response.json() if archivo["name"].endswith(".json")]

    for archivo in archivos:

        url = f"https://raw.githubusercontent.com/Zakaria-Dahi/TFG_UMA_2023_2204/main/data/{archivo}"

        try:
            response = requests.get(url, auth=(username, token))
            response.raise_for_status()
            data = response.json()
            backend_name = data[0]["name"]
            print(backend_name)

            backend_properties = data[0]["properties"]
            qubits = backend_properties["qubits"]
            for lista in qubits:
                for diccionario in lista:
                    diccionario.pop('date', None)
            
            print(qubits)

            gates = backend_properties["gates"]
            
            for gate in gates:
                for item in gate["parameters"]:
                    item.pop("date")
            
            #print(gates)

            #Unir los datos y meterlos en la bd

        except Exception as e:
            print(f"Error: {e}")

#descargar_ficheros()

'''
cliente = MongoClient("mongodb+srv://Marina:mongoTFG@tfg.qet3gme.mongodb.net/")
db = cliente.TFG

colleccion = db.procesado

documento = {
    "clave" : "prueba"
}

resultado_insercion = colleccion.insert_one(documento)

cliente.close()
'''


from pymongo import MongoClient

# Configuración de MongoDB Atlas (reemplaza con tus propios valores)
mongo_uri = "mongodb+srv://Marina:mongoTFG@tfg.qet3gme.mongodb.net/"
client = MongoClient(mongo_uri)

# Nombre de la colección en MongoDB Compass
collection_name_Destino = "procesado"
collection_name_Origen = "data"

# Conectarse a la base de datos en MongoDB Atlas
db = client["TFG"]

# Borro la colección por si tenía algún dato
db[collection_name_Destino].drop()
print("Colección borrada con éxito")

datos = db[collection_name_Origen].find()
#numero_elementos = len(datos)
#print(numero_elementos)
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
    collection = db[collection_name_Destino]
    collection.insert_one(dato)

print("Se han seleccionado los datos correctamente")


'''
    gates = dato['properties']['gates']

    gates_sin_atributos = []
    for gate in gates:
        gates_sin_atributo = [] 
        for g in gate['parameters']:
            if g['name'] == 'gate_error' or g['name'] == 'gate_length':
                gates_sin_atributo.append(g)  # Agrega el qubit a la lista si cumple con las condiciones
        gates_sin_atributos.append(gates_sin_atributo)
        dato['properties']['gates'] = gates_sin_atributos
'''  
