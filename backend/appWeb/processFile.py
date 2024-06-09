import statistics


def calcMedia(datos, nqubit, atributo):
    media = 0
    cont = 0

    for dato in datos:
        if nqubit > 0:
            if len(dato['qubits']) == nqubit:
                for gate in dato['parameters']:
                    if gate['name'] == 'gate_error':
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
                    valores.append(qubit['value'])
    valores.sort()
    n = len(valores)
    
    if n % 2 == 0:
        mediana = (valores[n//2 - 1] + valores[n//2]) / 2
    else:
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
        return None

    desviacion_estandar = statistics.stdev(valores)
    return desviacion_estandar

def processFile(file):

    file_data = file[0]

    name = file_data['name']

    qubits = file_data['properties']['qubits']
    qubits_derivados = []

    gates = file_data['properties']['gates']
    gates_derivados = []
        
    atributos = ["T1", "T2", "prob_meas0_prep1", "prob_meas1_prep0", "readout_error", "gate_error", "gate_length"]
    nqubits = [1, 2]

    for atributo in atributos:

        if atributo not in ["gate_error", "gate_length"]:

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
            
    return name, qubits_derivados, gates_derivados


