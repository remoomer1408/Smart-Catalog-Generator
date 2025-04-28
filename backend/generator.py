import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def process_csv_file(df):
    results = []

    for _, row in df.iterrows():
        product_name = row.get("product_name") or "Generic Product"

        prompt = f"""
        Generate a product title, a short but compelling description, and 3 bullet points for SEO from the product name: "{product_name}"

        Respond in JSON format like:
        {{
            "title": "...",
            "description": "...",
            "features": ["...", "...", "..."]
        }}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    { "role": "user", "content": prompt }
                ],
                temperature=0.7,
                max_tokens=300
            )

            content = response.choices[0].message.content.strip()
            generated = json.loads(content)  # parse clean JSON
        
        except Exception as e:
            generated = {
                "title": product_name,
                "description": "AI generation failed",
                "features": [],
                "error": str(e), 
                "product_name": product_name
            }

        results.append(generated)

    return results