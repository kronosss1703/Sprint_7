import allure
import pytest
import requests
from helpers.data_generator import generate_random_string
from data.messages import COURIER_CREATE_DUPLICATE, COURIER_CREATE_MISSING_DATA
from conftest import BASE_URL

@allure.suite("Создание курьера")
class TestCreateCourier:

    @allure.title("Курьера можно создать")
    def test_create_courier_success(self):
        login = generate_random_string()
        password = generate_random_string()
        first_name = generate_random_string()
        payload = {"login": login, "password": password, "firstName": first_name}
        with allure.step("Отправить запрос на создание курьера"):
            response = requests.post(f"{BASE_URL}/courier", data=payload)
        with allure.step("Проверить код ответа и тело"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self, new_courier):
        payload = {
            "login": new_courier["login"],
            "password": new_courier["password"],
            "firstName": new_courier["firstName"]
        }
        with allure.step("Отправить запрос на создание такого же курьера"):
            response = requests.post(f"{BASE_URL}/courier", data=payload)
        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 409
            assert response.json().get("message") == COURIER_CREATE_DUPLICATE

    @allure.title("Обязательные поля логин, пароль – без одного из них ошибка")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field):
        payload = {
            "login": generate_random_string(),
            "password": generate_random_string(),
            "firstName": generate_random_string()
        }
        del payload[missing_field]
        with allure.step(f"Отправить запрос без поля {missing_field}"):
            response = requests.post(f"{BASE_URL}/courier", data=payload)
        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json().get("message") == COURIER_CREATE_MISSING_DATA

    @allure.title("Создание курьера с уже существующим логином возвращает ошибку")
    def test_create_courier_existing_login_fails(self, new_courier):
        payload = {
            "login": new_courier["login"],
            "password": generate_random_string(),
            "firstName": generate_random_string()
        }
        with allure.step("Отправить запрос с существующим логином"):
            response = requests.post(f"{BASE_URL}/courier", data=payload)
        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 409
            assert COURIER_CREATE_DUPLICATE in response.json().get("message")