# backend/generator.py
def process_csv_file(df):
    generated = []
    for _, row in df.iterrows():
        product_name = row.get("Product Name", "Unnamed Product")
        category = row.get("Category", "General")

        entry = {
            "product_name": product_name,
            "title": f"Top-Quality {product_name}",
            "description": f"This {product_name} in the {category} category is perfect for modern needs.",
            "features": [
                f"Premium build for long-lasting use",
                f"Perfect for {category.lower()} enthusiasts",
                "Designed with care and efficiency"
            ],
            "tags": [product_name.lower(), category.lower(), "premium", "best seller"]
        }
        generated.append(entry)

    return generated
