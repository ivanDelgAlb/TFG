from qiskit_ibm_provider import IBMProvider
from datetime import datetime
import schedule
import time
import json

def obtener_informacion():
    # Cargar el proveedor de IBM Quantum
    provider = IBMProvider(token='4fdcd337fa47374d321d5f6d9fcd74c771cdc846e23e51f7d1256ce4839a44dfbc543b009a3fd6111ce286e9ec69b15e943a4a2f5b15291c98394127a22c82df')

    # Obtener la lista de backends disponibles
    backends = provider.backends(simulator=False)

    fecha_actual = datetime.now()
    # Crear el nombre del fichero con el timestamp
    nombre_archivo = fecha_actual.strftime("%Y-%m-%d_%H-%M-%S.json")

    lista_backends = []

    for backend in backends:
        try:
            # Obtener informacion del backend
            backend_obtenido = provider.get_backend(name=backend.name)
            
            partes = backend_obtenido.backend_version.split('.')
            primer_numero = int(partes[0])

            # Crear diccionario para el backend
            diccionario_backend = {}
            diccionario_backend['name'] = backend.name
            diccionario_backend['version'] = primer_numero

            # Saco las propiedades
            properties = backend_obtenido.properties().to_dict()

            # Formateo la fecha para que sea JSON serializable
            last_update_date = properties['last_update_date'].strftime('%Y-%m-%d %H:%M:%S')
            properties['last_update_date'] = last_update_date

            # Eliminar la fecha de los qubits
            qubits = properties['qubits']
            qubits_serializados = [[{'date': item['date'].strftime('%Y-%m-%d %H:%M:%S'), 'name': item['name'], 'unit': item['unit'], 'value': item['value']} for item in qubit] for qubit in qubits]
            properties['qubits'] = qubits_serializados

            # Eliminar la fecha de gate
            gates = properties['gates']
            for gate in gates:
                parameters = gate['parameters']
                parameters_serializados = [{'date': item['date'].strftime('%Y-%m-%d %H:%M:%S'), 'name': item['name'], 'unit': item['unit'], 'value': item['value']} for item in parameters]
                gate['parameters'] = parameters_serializados
            properties['gates'] = gates

            # Eliminar la fecha de general
            general = properties['general']
            general_serializados = [{'date': item['date'].strftime('%Y-%m-%d %H:%M:%S'), 'name': item['name'], 'unit': item['unit'], 'value': item['value']} for item in general]
            properties['general'] = general_serializados

            diccionario_backend['properties'] = properties

            # Verificar si el primer numero es 2
            if primer_numero == 2:
                diccionario_backend['configuration'] = backend_obtenido.configuration()
            else:
                diccionario_backend['configuration'] = None

            # Meter el diccionario en la lista
            lista_backends.append(diccionario_backend)

        except Exception as e:
            fichero_errores = "errores.txt"
            with open(fichero_errores, 'a') as errores:
                errores.write("Error: {}\n".format(e))
                errores.write("Fecha: " + str(fecha_actual) + "\n")
                errores.write("Backend: " + backend.name + "\n")

    # Escribir en el fichero la lista en formato JSON
    with open(nombre_archivo, 'a') as archivo:
        for backend_info in lista_backends:
            backend_info['properties']['last_update_date'] = str(backend_info['properties']['last_update_date'])
        json.dump(lista_backends, archivo)

#Agregar registro de inicio
fichero_salidas = "registro.txt"
with open(fichero_salidas, 'a') as fichero:
    fichero.write("Programa iniciado.\n")

obtener_informacion()

# Programar la ejecucion cada dos horas
schedule.every(2).hours.do(obtener_informacion)

# Bucle principal
while True:
    with open(fichero_salidas, 'a') as fichero:
        fichero.write("Esperando proxima ejecucion.\n")
    schedule.run_pending()
    time.sleep(60)

