from http.client import HTTPException
import pymongo
import os
import requests
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
DB_PASSWORD = os.getenv("DB_PASSWORD")

client = pymongo.MongoClient(f"mongodb+srv://syedmaisum1:{DB_PASSWORD}@thaqalayn-noor.rri8t2j.mongodb.net/?retryWrites=true&w=majority&appName=thaqalayn-noor")
db = client['thaqalayn-noor']
collection = db['data']

def find_hadith(url):
    hadith = collection.find_one({"thaqURL": url},
                                {
                                    "_id": 0,
                                    "thaqBookId": 1,
                                    "thaqText": 1,
                                    "thaqURL": 1,
                                    "noorText": 1,
                                    "noorBookTitle": 1,
                                    "noorURL": 1
                                })

    if not hadith:
        return HTTPException(status_code=404, detail="Hadith not found")
    
    return hadith

    