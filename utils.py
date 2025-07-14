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
    doc = collection.find_one({"thaqURL": url}, {"_id": 0, "noorId": 1})
    if not doc:
        print("No matching hadith found in database")
        return None

    id = doc["noorId"]

    url = f"https://hadith.inoor.ir/service/api/hadith/HadithRejalList/v2?hadithId={id}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to call Noor API: {response.status_code}")
        return None

    data = response.json()
    sanad_list = data.get("data", {}).get("sanadList", [])

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

            if ravi_list:
                narrators = []
                for ravi in ravi_list:
                    ravi_id = ravi.get("raviId")
                    narrator_name = ravi.get("hint")
                    narrator = get_narrator(ravi_id, data.get("data", {}).get("raviList", []))
                    narrator['name'] = narrator_name
                    narrators.append(narrator)
                
                chain.append({
                    "title": item.get("title"),
                    "narrators": narrators,
                    "is_narrator": True
                })
            
            else:
                chain.append({
                    "title": item.get("title"),
                    "is_narrator": False
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
