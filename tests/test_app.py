from fastapi.testclient import TestClient

from app.main import app


def test_get_restaurant():
    with TestClient(app) as client:
        response = client.get("/restaurants/99fe5fa3-16aa-44fa-8ee2-33bad84ef3c8")

    assert response.status_code == 200
    assert response.json() == {
        "name": "Ramen house",
        "description": "Japanese ramen",
        "id": "99fe5fa3-16aa-44fa-8ee2-33bad84ef3c8",
        "location": {
            "city": "Helsinki",
            "coordinates": {"lat": 60.169934599421396, "lon": 24.941786527633663},
        },
    }


def test_get_restaurant_returns_not_found_when_not_legit_id():
    with TestClient(app) as client:
        response = client.get("/restaurants/this-should-not-exist")

    assert response.status_code == 404
    assert {"detail": "Restaurant not found"} == response.json()
