import requests
from pymongo import MongoClient
from datetime import datetime

# Configuración de MongoDB Atlas (reemplaza con tus propios valores)
mongo_uri_part1 = "mongodb+srv://Marina:mongoTFG@tfg.qet3gme.mongodb.net/"
client_part1 = MongoClient(mongo_uri_part1)

mongo_uri_part2 = "mongodb+srv://marinasayago:TFG@tfg.fo8wxgc.mongodb.net/"
client_part2 = MongoClient(mongo_uri_part2)

# Ruta al directorio que contiene los archivos JSON en el repositorio de GitHub
github_repo_url = "https://github.com/Zakaria-Dahi/TFG_UMA_2023_2204"
data_directory = "data"

# Nombre de la colección en MongoDB Compass
collection_name = "data"

github_username = "marinasayago"
github_token = "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"

# Conectarse a la base de datos en MongoDB Atlas
db_part1 = client_part1["TFG"]
db_part2 = client_part2["TFG"]

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
#Datos insertados con éxito para el archivo: 2024-04-18_00-19-04.json
for file in files:

    try:
        # Modifica la URL para apuntar a la versión RAW del archivo en GitHub
        raw_url = f"https://raw.githubusercontent.com/Zakaria-Dahi/TFG_UMA_2023_2204/main/data/{file}"

        response = requests.get(raw_url, auth=(github_username, github_token))
        response.raise_for_status()  # Verificar si hay errores en la respuesta HTTP
        json_data = response.json()

        fecha_str = file.split(".")[0].replace("_", " ")

        # Convertir la cadena de fecha en un objeto datetime
        fecha_objeto = datetime.strptime(fecha_str, "%Y-%m-%d %H-%M-%S")

        # Formatear la fecha en el formato deseado
        fecha_formateada = fecha_objeto.strftime("%Y-%m-%d %H:%M:%S")

        for documento in json_data:
            documento['date'] = fecha_formateada
        
        # Insertar datos en la colección de MongoDB Compass
        if (fecha_objeto < datetime.strptime("2024-04-15 00-00-00", "%Y-%m-%d %H-%M-%S")) :       
            collection = db_part1[collection_name]  
            if(collection.find_one({"date": fecha_formateada}) == None) :  
                collection.insert_many(json_data)
                print(f"Datos insertados con éxito para el archivo: {file}")
            else: 
                print("Ya existe ese fichero")
        else : 
            print("HOLA")
            collection = db_part2[collection_name]
            if(collection.find_one({"date": fecha_formateada}) == None) : 
                collection.insert_many(json_data)
                print(f"Datos insertados con éxito para el archivo: {file}")
            else: 
                print("Ya existe ese fichero")


    except Exception as e:
        print(f"Error: {e}")



print("Proceso completado.")