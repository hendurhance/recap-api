from app.utils.handle_json_file import read_json_file
import os
from fastapi import HTTPException, status

def validate(category: str):
    categories = read_json_file("categories.json", os.path.join(
        os.getcwd(), "app", "news", "validator"))
    category_lower = category.lower()
    for c in categories:
        if c["category"].lower() == category_lower:
            return True
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category")


def get_source_and_url(category: str):
    validate(category)
    categories = read_json_file("categories.json", os.path.join(
        os.getcwd(), "app", "news", "validator"))
    category_lower = category.lower()
    for c in categories:
        if c["category"].lower() == category_lower:
            return {"source": c["source"], "url": c["url"]}
