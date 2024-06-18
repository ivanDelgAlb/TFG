import requests
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

origin_mongo_uri = os.getenv("MONGO_URI_MARINA_PART1")
destination_mongo_uri = os.getenv("MONGO_URI_IVAN_PART1")

mongo_uri_part1 = os.getenv("MONGO_URI_MARINA_PART1")
client_part1 = MongoClient(mongo_uri_part1)

mongo_uri_part2 = os.getenv("MONGO_URI_MARINA_PART2")
client_part2 = MongoClient(mongo_uri_part2)

mongo_uri_part3 = os.getenv("MONGO_URI_MARINA_PART3")
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
print("Authentication completed")

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

        str_date = file.split(".")[0].replace("_", " ")

        object_date = datetime.strptime(str_date, "%Y-%m-%d %H-%M-%S")

        formatted_date = object_date.strftime("%Y-%m-%d %H:%M:%S")

        for document in json_data:
            document['date'] = formatted_date
        
        if object_date < datetime.strptime("2024-04-15 00-00-00", "%Y-%m-%d %H-%M-%S"):
            collection = db_part1[collection_name]  
            if collection.find_one({"date": formatted_date}) is None:
                collection.insert_many(json_data)
                print(f"Data inserted for file: {file}")
            else: 
                print("File already exists")
        elif object_date < datetime.strptime("2024-05-28 00-00-00", "%Y-%m-%d %H-%M-%S"):
            collection = db_part2[collection_name]
            if collection.find_one({"date": formatted_date}) is None:
                collection.insert_many(json_data)
                print(f"Data inserted for file: {file}")
            else: 
                print("File already exists")
        else:
            collection = db_part3[collection_name]
            if collection.find_one({"date": formatted_date}) is None:
                collection.insert_many(json_data)
                print(f"Data inserted for file: {file}")
            else: 
                print("File already exists")

    except Exception as e:
        print(f"Error: {e}")

print("Process completed.")
