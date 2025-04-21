from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from generator import process_csv_file
import pandas as pd

app = FastAPI()

# Enabling CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-catalog/")
async def generate_catalog(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    results = process_csv_file(df)
    return {"data": results}
