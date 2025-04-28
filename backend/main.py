from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import List
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "AI Smart Catalog Generator Backend"}

@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return JSONResponse(status_code=400, content={"message": "Please upload a CSV file"})
    try:
        contents = await file.read()
        decoded_contents = contents.decode("utf-8")
        lines = decoded_contents.strip().split('\n')
        headers = [header.strip() for header in lines[0].split(',')]
        return {"filename": file.filename, "headers": headers}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error processing file: {e}"})

async def generate_description(prompt: str):
    try:
        response = await openai.chat.completions.create(
            model="gpt-3.5-turbo",  # You can choose a different model
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,  # Adjust as needed
            n=1,  # Generate one description
            stop=None,
            temperature=0.7,  # Adjust for creativity
        )
        if response.choices:
            return response.choices[0].message.content.strip()
        else:
            return "Error: Could not generate description."
    except Exception as e:
        return f"Error communicating with OpenAI: {e}"

@app.post("/generate_catalog")
async def generate_catalog(
    csv_file: UploadFile = File(...),
    prompt_template: str = Form(...),
    style_guidelines: str = Form(None),
    additional_context: str = Form(None)
):
    if not csv_file.filename.endswith(".csv"):
        return JSONResponse(status_code=400, content={"message": "Please upload a CSV file"})

    try:
        contents = await csv_file.read()
        decoded_contents = contents.decode("utf-8")
        lines = decoded_contents.strip().split('\n')
        headers = [header.strip() for header in lines[0].split(',')]
        data = []
        for line in lines[1:]:
            values = [value.strip() for value in line.split(',')]
            if len(values) == len(headers):
                data.append(dict(zip(headers, values)))

        generated_products = []
        for item in data:
            prompt = prompt_template
            for header, value in item.items():
                prompt = prompt.replace(f"{{{header}}}", value)

            if style_guidelines:
                prompt += f"\n\nStyle Guidelines: {style_guidelines}"
            if additional_context:
                prompt += f"\n\nAdditional Context: {additional_context}"

            description = await generate_description(prompt)
            generated_products.append({**item, "description": description})

        return {"generated_catalog": generated_products}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error processing file: {e}"})