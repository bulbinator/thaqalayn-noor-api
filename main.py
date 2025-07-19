from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils import find_hadith, get_chain

app = FastAPI(
    title="Thaqalayn-Noor API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Go to /docs"}

@app.get("/search")
async def search(url: str = Query(...)):
    return find_hadith(url)

@app.get("/chain")
async def chain(url: str = Query(...)):
    return get_chain(url)
