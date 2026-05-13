import pytest
import requests
import random
import string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def register_new_courier():
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()
    payload = {"login": login, "password": password, "firstName": first_name}
    response = requests.post(f"{BASE_URL}/courier", data=payload)
    if response.status_code == 201:
        login_payload = {"login": login, "password": password}
        login_response = requests.post(f"{BASE_URL}/courier/login", data=login_payload)
        courier_id = login_response.json().get("id") if login_response.status_code == 200 else None
        return {"login": login, "password": password, "firstName": first_name, "id": courier_id}
    return None

def delete_courier(courier_id):
    if courier_id:
        response = requests.delete(f"{BASE_URL}/courier/{courier_id}")
        return response.status_code == 200 and response.json().get("ok") is True
    return False

@pytest.fixture
def new_courier():
    courier_data = register_new_courier()
    yield courier_data
    if courier_data and courier_data.get("id"):
        delete_courier(courier_data["id"])

@pytest.fixture
def created_order():
    payload = {
        "firstName": "Тест",
        "lastName": "Тестов",
        "address": "Москва, ул. Тестовая, 1",
        "metroStation": 4,
        "phone": "+79991234567",
        "rentTime": 3,
        "deliveryDate": "2025-05-20",
        "comment": "Тестовый заказ",
        "color": ["BLACK"]
    }
    response = requests.post(f"{BASE_URL}/orders", json=payload)
    track = response.json().get("track") if response.status_code == 201 else None
    yield track