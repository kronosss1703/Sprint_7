import requests
from helpers.data_generator import generate_random_string

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

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