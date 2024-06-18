from qiskit_ibm_provider import IBMProvider
from datetime import datetime
import schedule
import time
import json
from git import Repo


def obtain_info():
    repo = Repo.init('/home/zak-ubuntu/Desktop/TFG_UMA_2023_2024')
    repo.git.add(all=True)
    commit_name = "Commit done on: " + str(datetime.now())
    repo.index.commit(commit_name)
    origin = repo.remote('origin')
    res = origin.push()
    provider = IBMProvider(token='4fdcd337fa47374d321d5f6d9fcd74c771cdc846e23e51f7d1256ce4839a44dfbc543b009a3fd6111ce286e9ec69b15e943a4a2f5b15291c98394127a22c82df')

    backends = provider.backends(simulator=False)

    current_date = datetime.now()
    file_name = current_date.strftime("%Y-%m-%d_%H-%M-%S.json")
    file_name = "data/" + file_name

    backends_list = []

    for backend in backends:
        try:
            obtained_backend = provider.get_backend(name=backend.name)
            
            parts = obtained_backend.backend_version.split('.')
            version = int(parts[0])

            backends_dictionary = {'name': backend.name, 'version': version}

            properties = obtained_backend.properties().to_dict()

            last_update_date = properties['last_update_date'].strftime('%Y-%m-%d %H:%M:%S')
            properties['last_update_date'] = last_update_date

            qubits = properties['qubits']
            serialized_qubits = [[{'date': item['date'].strftime('%Y-%m-%d %H:%M:%S'), 'name': item['name'], 'unit': item['unit'], 'value': item['value']} for item in qubit] for qubit in qubits]
            properties['qubits'] = serialized_qubits

            gates = properties['gates']
            for gate in gates:
                parameters = gate['parameters']
                serialized_parameters = [{'date': item['date'].strftime('%Y-%m-%d %H:%M:%S'), 'name': item['name'], 'unit': item['unit'], 'value': item['value']} for item in parameters]
                gate['parameters'] = serialized_parameters
            properties['gates'] = gates

            general = properties['general']
            serialized_general = [{'date': item['date'].strftime('%Y-%m-%d %H:%M:%S'), 'name': item['name'], 'unit': item['unit'], 'value': item['value']} for item in general]
            properties['general'] = serialized_general

            backends_dictionary['properties'] = properties

            if version == 2:
                backends_dictionary['configuration'] = obtained_backend.configuration()
            else:
                backends_dictionary['configuration'] = None

            backends_list.append(backends_dictionary)

        except Exception as e:
            errors_file_name = "errores.txt"
            with open(errors_file_name, 'a') as errors_file:
                errors_file.write("Error: {}\n".format(e))
                errors_file.write("Date: " + str(current_date) + "\n")
                errors_file.write("Backend: " + backend.name + "\n")

    with open(file_name, 'a') as file_backends:
        for backend_info in backends_list:
            backend_info['properties']['last_update_date'] = str(backend_info['properties']['last_update_date'])
        json.dump(backends_list, file_backends)


prints_file_name = "registro.txt"
with open(prints_file_name, 'a') as file:
    file.write("Program started.\n")

obtain_info()

schedule.every(2).hours.do(obtain_info)

while True:
    with open(prints_file_name, 'a') as file:
        file.write("Waiting next execution.\n")
    schedule.run_pending()
    time.sleep(60)
