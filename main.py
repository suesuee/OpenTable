from fastapi import FastAPI, Query, HTTPException
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")

app = FastAPI()
SPOONACULAR_BASE_URL = "https://api.spoonacular.com/recipes/findByIngredients"


@app.get("/recipes/", tags=["Recipes"])
def get_recipes(
    ingredients: str = Query(..., description="Comma-separated list of ingredients"),
    number: int = Query(5, description="Number of recipes to fetch"),
):
    # Build the request to Spoonacular API
    response = requests.get(
        SPOONACULAR_BASE_URL,
        params={
            "ingredients": ingredients,
            "number": number,
            "apiKey": SPOONACULAR_API_KEY,
        },
    )

    # Check if the API call was successful
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch recipes from Spoonacular API",
        )
    return response.json()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
