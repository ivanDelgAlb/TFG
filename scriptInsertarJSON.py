import requests
from pymongo import MongoClient

# Configuración de MongoDB Atlas (reemplaza con tus propios valores)
mongo_uri = "mongodb+srv://Marina:mongoTFG@tfg.qet3gme.mongodb.net/"
client = MongoClient(mongo_uri)

# Ruta al directorio que contiene los archivos JSON en el repositorio de GitHub
github_repo_url = "https://github.com/Zakaria-Dahi/TFG_UMA_2023_2204"
data_directory = "data"

# Nombre de la colección en MongoDB Compass
collection_name = "data"



github_username = "marinasayago"
github_token = "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"

# Conectarse a la base de datos en MongoDB Atlas
db = client["TFG"]

# Borro la colección por si tenía algún dato
db[collection_name].drop()
print("Colección borrada con éxito")

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
for file in files:

    try:
        # Modifica la URL para apuntar a la versión RAW del archivo en GitHub
        raw_url = f"https://raw.githubusercontent.com/Zakaria-Dahi/TFG_UMA_2023_2204/main/data/{file}"

        response = requests.get(raw_url, auth=(github_username, github_token))
        response.raise_for_status()  # Verificar si hay errores en la respuesta HTTP
        json_data = response.json()
        
        # Insertar datos en la colección de MongoDB Compass
        collection = db[collection_name]
        collection.insert_many(json_data)
        print(f"Datos insertados con éxito para el archivo: {file}")

    except Exception as e:
        print(f"Error: {e}")



print("Proceso completado.")