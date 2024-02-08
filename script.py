from qiskit_ibm_provider import IBMProvider
from datetime import datetime
import schedule
import time


def getInformation():
        # Cargar tu cuenta de IBM Quantum Experience
    # Asegúrate de reemplazar 'tu_token' con tu token real
    provider = IBMProvider(token='4fdcd337fa47374d321d5f6d9fcd74c771cdc846e23e51f7d1256ce4839a44dfbc543b009a3fd6111ce286e9ec69b15e943a4a2f5b15291c98394127a22c82df')

    # Obtener la lista de backends disponibles y operativos
    backends = provider.backends(simulator=False, operational=True)

    fecha_actual = datetime.now()
    nombre_archivo = fecha_actual.strftime("%d-%m-%Y_%H;%M;%S.txt")

    for backend in backends:
        try:
            # Obtener información actualizada del backend
            backendObtained = provider.get_backend(name=backend.name)
            
            partes = backendObtained.backend_version.split('.')
            primer_numero = int(partes[0])

            # Verificar si el primer número es 1 o 2
            if primer_numero in [1, 2]:
                with open(nombre_archivo, 'w') as archivo:
                    try:
                        properties = backendObtained.properties()
                        #print("Escribiendo:", properties.to_dict())
                        archivo.write(str(properties.to_dict()))
                    except TypeError as e:
                        print(f"Error al escribir propiedades: {e}")

            # Verificar si el primer número es 2
            if primer_numero == 2:
                with open(nombre_archivo, 'a') as archivo:  # Usar 'a' para agregar al archivo existente
                    configuration = backendObtained.configuration()
                    archivo.write(str(configuration.to_dict()))


            #with open(nombre_archivo, 'w') as archivo:  # Usar 'a' para agregar al archivo existente
            #      qubitProperties = backendObtained.qubit_properties(qubit)
            #     archivo.write(str(qubitProperties.to_dict()))

        except Exception as e:
            print(f"Error: {e}")


#Agregar registro de inicio
print("Programa iniciado.")

# Ejecutar inmediatamente al inicio
getInformation()

# Programar la ejecución cada dos horas
schedule.every(2).hours.do(getInformation)

# Bucle principal
while True:
    # Agregar registro de espera
    print("Esperando próxima ejecución...")
    schedule.run_pending()
    # Considerar ajustar el tiempo de espera según tus necesidades
    time.sleep(60)  # Esperar 1 minuto antes de verificar de nuevo
