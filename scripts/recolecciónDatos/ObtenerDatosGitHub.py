from qiskit_ibm_provider import IBMProvider
from datetime import datetime
import schedule
import time
import json
from git import Repo


def obtener_informacion():
    repo = Repo.init('/home/zak-ubuntu/Desktop/TFG_UMA_2023_2024')
    repo.git.add(all=True)
    commit_name = "Commit done on: " + str(datetime.now())
    repo.index.commit(commit_name)
    origin = repo.remote('origin')
    res = origin.push()
    provider = IBMProvider(token='4fdcd337fa47374d321d5f6d9fcd74c771cdc846e23e51f7d1256ce4839a44dfbc543b009a3fd6111ce286e9ec69b15e943a4a2f5b15291c98394127a22c82df')

    backends = provider.backends(simulator=False)

    fecha_actual = datetime.now()
    nombre_archivo = fecha_actual.strftime("%Y-%m-%d_%H-%M-%S.json")
    nombre_archivo = "data/" + nombre_archivo

    lista_backends = []

    for backend in backends:
        try:
            backend_obtenido = provider.get_backend(name=backend.name)
            
            partes = backend_obtenido.backend_version.split('.')
            primer_numero = int(partes[0])

            diccionario_backend = {}
            diccionario_backend['name'] = backend.name
            diccionario_backend['version'] = primer_numero

            properties = backend_obtenido.properties().to_dict()

            last_update_date = properties['last_update_date'].strftime('%Y-%m-%d %H:%M:%S')
            properties['last_update_date'] = last_update_date

            qubits = properties['qubits']
            qubits_serializados = [[{'date': item['date'].strftime('%Y-%m-%d %H:%M:%S'), 'name': item['name'], 'unit': item['unit'], 'value': item['value']} for item in qubit] for qubit in qubits]
            properties['qubits'] = qubits_serializados

            gates = properties['gates']
            for gate in gates:
                parameters = gate['parameters']
                parameters_serializados = [{'date': item['date'].strftime('%Y-%m-%d %H:%M:%S'), 'name': item['name'], 'unit': item['unit'], 'value': item['value']} for item in parameters]
                gate['parameters'] = parameters_serializados
            properties['gates'] = gates

            general = properties['general']
            general_serializados = [{'date': item['date'].strftime('%Y-%m-%d %H:%M:%S'), 'name': item['name'], 'unit': item['unit'], 'value': item['value']} for item in general]
            properties['general'] = general_serializados

            diccionario_backend['properties'] = properties

            if primer_numero == 2:
                diccionario_backend['configuration'] = backend_obtenido.configuration()
            else:
                diccionario_backend['configuration'] = None

            lista_backends.append(diccionario_backend)

        except Exception as e:
            fichero_errores = "errores.txt"
            with open(fichero_errores, 'a') as errores:
                errores.write("Error: {}\n".format(e))
                errores.write("Fecha: " + str(fecha_actual) + "\n")
                errores.write("Backend: " + backend.name + "\n")

    with open(nombre_archivo, 'a') as archivo:
        for backend_info in lista_backends:
            backend_info['properties']['last_update_date'] = str(backend_info['properties']['last_update_date'])
        json.dump(lista_backends, archivo)

fichero_salidas = "registro.txt"
with open(fichero_salidas, 'a') as fichero:
    fichero.write("Programa iniciado.\n")

obtener_informacion()

schedule.every(2).hours.do(obtener_informacion)

while True:
    with open(fichero_salidas, 'a') as fichero:
        fichero.write("Esperando proxima ejecucion.\n")
    schedule.run_pending()
    time.sleep(60)