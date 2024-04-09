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
