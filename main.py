from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import BaseModel
import httpx

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()


@app.get("/pokemons/")
async def read_items(limit: str | None = None):
    url = "https://pokeapi.co/api/v2/pokemon/"
    async with httpx.AsyncClient() as client:
        if limit:
            # If a query is specified, add it to the API request
            response = await client.get(f"{url}?limit={limit}")
        else:
            response = await client.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            results = response.json()
        else:
            # Handle potential errors in response
            results = {"error": "Failed to fetch data from PokeAPI", "status_code": response.status_code}
    
    return results


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict