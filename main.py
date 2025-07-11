from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from search import find_hadith

app = FastAPI(
    title="Thaqalayn-Noor API",
    version="1.0.0"
)

@app.get("/")
@app.head("/")
async def root():
    return {"message": "Go to /docs"}

@app.get("/search")
async def search(url):
    response = find_hadith(url)
    return JSONResponse(content=response)