import requests
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de MongoDB Atlas (reemplaza con tus propios valores)
mongo_uri_part1 = os.getenv("MONGO_URI_MARINA_PART1")
client_part1 = MongoClient(mongo_uri_part1)

mongo_uri_part2 = os.getenv("MONGO_URI_MARINA_PART2")
client_part2 = MongoClient(mongo_uri_part2)

# Ruta al directorio que contiene los archivos JSON en el repositorio de GitHub
github_repo_url = os.getenv("GITHUB_REPO")
data_directory = "data"

# Nombre de la colección en MongoDB Compass
collection_name = "data"

github_username = os.getenv("GITHUB_USERNAME")
github_token = os.getenv("GITHUB_TOKEN")

# Conectarse a la base de datos en MongoDB Atlas
db_part1 = client_part1["TFG"]
db_part2 = client_part2["TFG"]

# Autenticación con la API de GitHub
auth_url = "https://api.github.com/user"
auth_response = requests.get(auth_url, auth=(github_username, github_token))
auth_response.raise_for_status()
("Autenticación exitosa")

# Obtener la lista de archivos JSON en la carpeta del repositorio de GitHub
repo_contents_url = github_repo_url + {data_directory}
contents_response = requests.get(repo_contents_url, auth=(github_username, github_token))
contents_response.raise_for_status()

# Obtener nombres de archivos JSON
files = [file["name"] for file in contents_response.json() if file["name"].endswith(".json")]

# Iterar sobre los archivos y cargar los datos en MongoDB
#Datos insertados con éxito para el archivo: 2024-04-18_00-19-04.json
for file in files:

    try:
        # Modifica la URL para apuntar a la versión RAW del archivo en GitHub
        raw_url = os.getenv("GITHUB_RAW") + {file}

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
                (f"Datos insertados con éxito para el archivo: {file}")
            else: 
                ("Ya existe ese fichero")
        else : 
            ("HOLA")
            collection = db_part2[collection_name]
            if(collection.find_one({"date": fecha_formateada}) == None) : 
                collection.insert_many(json_data)
                (f"Datos insertados con éxito para el archivo: {file}")
            else: 
                ("Ya existe ese fichero")


    except Exception as e:
        (f"Error: {e}")



("Proceso completado.")