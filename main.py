from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from utils import find_hadith, get_chain

app = FastAPI(
    title="Thaqalayn-Noor API",
    version="1.0.0"
)

@app.get("/")
@app.head("/")
async def root():
    return {"message": "Go to /docs"}

@app.get("/search")
async def search(url: str = Query(description="Enter a thaqalayn.net/hadith URL. All books supported except for: Man la Yahduruhu al-Faqih, Kitab al-Duafa, Risalat al-Huquq, and Mujam al-Ahadith al-Mutabara.")):
    return find_hadith(url)

@app.get("/chain")
async def chain(url: str = Query(description="Enter a thaqalayn.net/hadith URL to get chain analysis. All books supported except for: Man la Yahduruhu al-Faqih, Kitab al-Duafa, Risalat al-Huquq, and Mujam al-Ahadith al-Mutabara.")):
    return get_chain(url)