import random
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
import uvicorn
from utils.pokemon import find_pokemon_body, find_pokemon_name, pokemon_wiki, find_pokemon_image, find_pokemon_image_from_api

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount static files for serving CSS/JS if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})

@app.get("/")
async def index(
    request: Request,
    name: str = Query(None, description="Name of the Pokémon"),
    height: float = Query(None, description="Height of the Pokémon in centimeters"),
    weight: float = Query(None, description="Weight of the Pokémon in kilograms"),
    tolerance: float = Query(0.1, description="Tolerance percentage for matching height and weight")
):
    pokemon_data = None
    nearby_pokemon = None
    random_pokemon = None
    error_message = None

    if name:
        zh_name, pokemon_type = find_pokemon_name(name)
        if zh_name:
            pokemon_row = pokemon_wiki(zh_name)
            if pokemon_row:
                eng_name, image_url = find_pokemon_image(pokemon_row)
                pokemon_data = {
                    "name": zh_name,
                    "type": pokemon_type,
                    "image_url": image_url,
                    "height": None,
                    "weight": None
                }
                
    if height is not None and weight is not None:
        try:
            nearby_pokemon = find_pokemon_body(height, weight, tolerance)  # Height is now in centimeters
            if nearby_pokemon:
                random_pokemon = random.choice(nearby_pokemon)
                # Fetch image URL for the randomly selected Pokémon
                random_pokemon_image_url = find_pokemon_image_from_api(random_pokemon["name"])
                random_pokemon["image_url"] = random_pokemon_image_url
            else:
                error_message = "查無寶可夢"
        except Exception as e:
            error_message = f"Failed to fetch Pokémon details: {str(e)}"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "pokemon_data": pokemon_data,
            "nearby_pokemon": nearby_pokemon,
            "random_pokemon": random_pokemon,
            "error_message": error_message
        }
    )

@app.get("/pokemon")
async def get_pokemon(name: str = Query(..., description="Name of the Pokémon")):
    zh_name, pokemon_type = find_pokemon_name(name)
    if zh_name:
        return JSONResponse(content={"name": zh_name, "type": pokemon_type})
    return JSONResponse(content={"error": "Pokémon not found"}, status_code=404)

@app.get("/nearby-pokemon")
async def nearby_pokemon(
    height: float = Query(..., description="Height of the Pokémon in meters"),
    weight: float = Query(..., description="Weight of the Pokémon in kilograms"),
    tolerance: float = Query(0.1, description="Tolerance percentage for matching height and weight")
):
    nearby_pokemon = find_pokemon_body(height, weight, tolerance)
    if nearby_pokemon:
        return JSONResponse(content={"nearby_pokemon": nearby_pokemon})
    return JSONResponse(content={"error": "No Pokémon found with similar height and weight"}, status_code=404)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
