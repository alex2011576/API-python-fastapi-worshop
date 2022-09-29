import json
import pathlib

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Restaurant API")


RESTAURANTS_BY_ID = {}


@app.on_event("startup")
def on_startup():
    print("READING THE RESTAURANTS FILE")
    data_file_path = pathlib.Path(__file__).parent / "restaurants.json"

    with open(data_file_path) as f:
        raw_data = json.load(f)

    for raw_restaurant in raw_data["restaurants"]:
        lon, lat = raw_restaurant["location"]
        restaurant_id = raw_restaurant["id"]
        restaurant = Restaurant(
            name=raw_restaurant["name"],
            description=raw_restaurant["description"],
            id=restaurant_id,
            location=Location(
                city=raw_restaurant["city"],
                coordinates=Coordinates(lon=lon, lat=lat),
            ),
        )
        RESTAURANTS_BY_ID[restaurant_id] = restaurant


@app.get("/")
def hello_world():
    return {"Hello": "Jerry"}


@app.get(
    "/showcase-features/{user_id}",
    summary="MY custom summary",
    description="My custom description",
)
def showcase_features(
    user_id: int = Path(description="my custom description"),
    debug: bool = Query(default=False, description="some description"),
):
    if debug:
        print("Now we are debugging")
    return {"foo": "bar", "user_id": user_id}


class Coordinates(BaseModel):
    lon: float
    lat: float


class Location(BaseModel):
    city: str
    coordinates: Coordinates


class Restaurant(BaseModel):
    name: str = Field(description="This is the name of the restaurant")
    description: str
    id: str
    location: Location


@app.get("/restaurants", response_model=list[Restaurant])
def get_restaurants():
    return list(RESTAURANTS_BY_ID.values())


@app.get("/restaurants/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: str):
    if restaurant_id in RESTAURANTS_BY_ID:
        return RESTAURANTS_BY_ID[restaurant_id]
    raise HTTPException(status_code=404, detail="Restaurant not found")
