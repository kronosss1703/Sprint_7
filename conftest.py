import pytest
import requests
from helpers.courier_api import register_new_courier, delete_courier
from data.order_data import BASE_ORDER_PAYLOAD

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

@pytest.fixture
def new_courier():
    courier_data = register_new_courier()
    yield courier_data
    if courier_data and courier_data.get("id"):
        delete_courier(courier_data["id"])

@pytest.fixture
def created_order():
    payload = BASE_ORDER_PAYLOAD.copy()
    payload["color"] = ["BLACK"]
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    track = response.json().get("track") if response.status_code == 201 else None
    yield track

@pytest.fixture
def created_order_no_color():
    payload = BASE_ORDER_PAYLOAD.copy()
    payload["color"] = []
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    track = response.json().get("track") if response.status_code == 201 else None
    yield track