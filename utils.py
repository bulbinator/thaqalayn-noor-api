from fastapi import HTTPException
import pymongo
import requests
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
DB_PASSWORD = os.getenv("DB_PASSWORD")

client = pymongo.MongoClient(f"mongodb+srv://syedmaisum1:{DB_PASSWORD}@thaqalayn-noor.rri8t2j.mongodb.net/?retryWrites=true&w=majority&appName=thaqalayn-noor")

db = client["thaqalayn-noor"]
collection = db["data"]

def get_narrator(ravi_id, ravi_list):
    for ravi in ravi_list:
        if ravi.get("raviId") == ravi_id:
            return ravi

def get_chain(url):
    hadith = collection.find_one({"thaqURL": url}, {"_id": 0, "chains": 1})
    if not hadith:
        print("No matching hadith found in database")
        return None
    sanad_list = hadith.get("chains", {}).get("data", {}).get("sanadList", [])

    if not sanad_list:
        print("No sanad list found")
        return None

    chains = []
    for sanad_item in sanad_list:
        chain = []
        sanad = sanad_item.get("sanad", [])
        for item in sanad:
            ravi_list = item.get("raviList")
            title = item.get("title")
            narrators = []

            if item.get("type") == 1:
                is_narrator = False
            else:
                is_narrator = True

            if ravi_list:
                for ravi in ravi_list:
                    ravi_id = ravi.get("raviId")
                    narrator_name = ravi.get("hint")
                    narrator = get_narrator(ravi_id, hadith.get("chains", {}).get("data", {}).get("raviList", []))
                    narrator['name'] = narrator_name
                    narrators.append(narrator)
                
            chain.append({
                "title": title,
                "narrators": narrators,
                "is_narrator": is_narrator
            })

        chains.append(chain)

    return chains


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
        raise HTTPException(status_code=404, detail="Please enter a valid thaqalayn.net/hadith URL")
    
    return hadith
