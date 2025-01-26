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
    ingredients: str = Query(
        ...,
        description="Comma-separated list of ingredients (e.g., apples,flour,sugar)",
    ),
    number: int = Query(5, description="Number of recipes to fetch (1-100)"),
    ranking: int = Query(
        1,
        description="1 to maximize used ingredients; 2 to minimize missing ingredients",
    ),
    ignorePantry: bool = Query(
        True, description="Whether to ignore pantry items like water, salt, etc."
    ),
):
    """
    Fetch recipes from Spoonacular API based on ingredients and additional parameters.

    - **ingredients**: Comma-separated list of ingredients (e.g., apples,flour,sugar).
    - **number**: Number of recipes to fetch (default: 10, max: 100).
    - **ranking**: 1 to maximize used ingredients, 2 to minimize missing ingredients.
    - **ignorePantry**: True to ignore pantry items like water, salt, etc.
    """

    # Build query parameters for Spoonacular API
    params = {
        "ingredients": ingredients,
        "number": number,
        "ranking": ranking,
        "ignorePantry": str(ignorePantry).lower(),  # Convert to "true" or "false"
        "apiKey": SPOONACULAR_API_KEY,
    }

    # Call Spoonacular API
    response = requests.get(SPOONACULAR_BASE_URL, params=params)

    # Check for successful response
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to fetch recipes from Spoonacular API",
        )

    return response.json()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# Run the server
# source venv/bin/activate
# uvicorn main:app --reload

# or # venv/bin/uvicorn main:app --reload
