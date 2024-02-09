from qiskit_ibm_provider import IBMProvider
from datetime import datetime
import schedule
import time

def obtener_informacion():
    # Cargar el proveedor de IBM Quantum
    provider = IBMProvider(token='4fdcd337fa47374d321d5f6d9fcd74c771cdc846e23e51f7d1256ce4839a44dfbc543b009a3fd6111ce286e9ec69b15e943a4a2f5b15291c98394127a22c82df')

    # Obtener la lista de backends disponibles
    backends = provider.backends(simulator=False)

    fecha_actual = datetime.now()
    # Crear el nombre del fichero con el timestamp
    nombre_archivo = fecha_actual.strftime("%d/%m/%Y_%H:%M:%S.txt")

    for backend in backends:
        try:
            # Obtener información del backend
            backend_obtenido = provider.get_backend(name=backend.name)

            partes = backend_obtenido.backend_version.split('.')
            primer_numero = int(partes[0])
            # Verificar si el primer número es 1 o 2
            if primer_numero in [1, 2]:
                with open(nombre_archivo, 'w') as archivo:
                    try:
                        properties = backend_obtenido.properties()
                        archivo.write(str(properties.to_dict()))
                    except TypeError as e:
                        print(f"Error al escribir propiedades: {e}")

            # Verificar si el primer número es 2
            if primer_numero == 2:
                with open(nombre_archivo, 'a') as archivo:
                    configuration = backend_obtenido.configuration()
                    archivo.write(str(configuration.to_dict()))


            #with open(nombre_archivo, 'w') as archivo:  # Usar 'a' para agregar al archivo existente
            #      qubitProperties = backend_obtenido.qubit_properties(qubit)
            #     archivo.write(str(qubitProperties.to_dict()))
        except Exception as e:
            print(f"Error: {e}")

#Agregar registro de inicio
print("Programa iniciado.")

# Programar la ejecución cada dos horas
schedule.every(2).hours.do(obtener_informacion)

# Bucle principal
while True:
    print("Esperando próxima ejecución...")
    schedule.run_pending()
    time.sleep(60)

