import requests
from pymongo import MongoClient
from datetime import datetime

mongo_uri_part1 = "mongodb+srv://Marina:mongoTFG@tfg.qet3gme.mongodb.net/"
client_part1 = MongoClient(mongo_uri_part1)

mongo_uri_part2 = "mongodb+srv://marinasayago:TFG@tfg.fo8wxgc.mongodb.net/"
client_part2 = MongoClient(mongo_uri_part2)

mongo_uri_part3 = "mongodb+srv://marinasayago2002:clavetfg@tfg-part3.jphrtkl.mongodb.net/"
client_part3 = MongoClient(mongo_uri_part3)

github_repo_url = "https://github.com/Zakaria-Dahi/TFG_UMA_2023_2204"
data_directory = "data"

collection_name = "data"

github_username = "marinasayago"
github_token = "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"

db_part1 = client_part1["TFG"]
db_part2 = client_part2["TFG"]
db_part3 = client_part3["TFG"]

auth_url = "https://api.github.com/user"
auth_response = requests.get(auth_url, auth=(github_username, github_token))
auth_response.raise_for_status()
print("Autenticación exitosa")

repo_contents_url = f"https://api.github.com/repos/Zakaria-Dahi/TFG_UMA_2023_2204/contents/{data_directory}"
contents_response = requests.get(repo_contents_url, auth=(github_username, github_token))
contents_response.raise_for_status()

files = [file["name"] for file in contents_response.json() if file["name"].endswith(".json")]

for file in files:

    try:
        raw_url = f"https://raw.githubusercontent.com/Zakaria-Dahi/TFG_UMA_2023_2204/main/data/{file}"

        response = requests.get(raw_url, auth=(github_username, github_token))
        response.raise_for_status()
        json_data = response.json()

        fecha_str = file.split(".")[0].replace("_", " ")

        fecha_objeto = datetime.strptime(fecha_str, "%Y-%m-%d %H-%M-%S")

        fecha_formateada = fecha_objeto.strftime("%Y-%m-%d %H:%M:%S")

        for documento in json_data:
            documento['date'] = fecha_formateada
        
        if (fecha_objeto < datetime.strptime("2024-04-15 00-00-00", "%Y-%m-%d %H-%M-%S")) :       
            collection = db_part1[collection_name]  
            if(collection.find_one({"date": fecha_formateada}) == None) :  
                collection.insert_many(json_data)
                print(f"Datos insertados con éxito para el archivo: {file}")
            else: 
                print("Ya existe ese fichero")
        elif (fecha_objeto < datetime.strptime("2024-05-28 00-00-00", "%Y-%m-%d %H-%M-%S")) : 
            collection = db_part2[collection_name]
            if(collection.find_one({"date": fecha_formateada}) == None) : 
                collection.insert_many(json_data)
                print(f"Datos insertados con éxito para el archivo: {file}")
            else: 
                print("Ya existe ese fichero")
        else:
            collection = db_part3[collection_name]
            if(collection.find_one({"date": fecha_formateada}) == None) : 
                collection.insert_many(json_data)
                print(f"Datos insertados con éxito para el archivo: {file}")
            else: 
                print("Ya existe ese fichero")

    except Exception as e:
        print(f"Error: {e}")

print("Proceso completado.")