import allure
import pytest
import requests
from helpers.data_generator import generate_random_string
from data.messages import COURIER_LOGIN_MISSING_DATA, COURIER_LOGIN_NOT_FOUND
from conftest import BASE_URL

@allure.suite("Логин курьера")
class TestLoginCourier:

    @allure.title("Курьер может авторизоваться")
    def test_login_success(self, new_courier):
        payload = {"login": new_courier["login"], "password": new_courier["password"]}
        with allure.step("Отправить запрос на авторизацию"):
            response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        with allure.step("Проверить код ответа и наличие id"):
            assert response.status_code == 200
            assert "id" in response.json()
            assert isinstance(response.json()["id"], int)

    @allure.title("Для авторизации нужны оба поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, missing_field, new_courier):
        payload = {"login": new_courier["login"], "password": new_courier["password"]}
        del payload[missing_field]
        with allure.step(f"Отправить запрос без поля {missing_field}"):
            response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 400, f"API bug: expected 400, got {response.status_code}"
            assert response.json().get("message") == COURIER_LOGIN_MISSING_DATA

    @allure.title("Ошибка при неверном логине или пароле")
    @pytest.mark.parametrize("wrong_field,value", [
        ("login", "wrong_login"),
        ("password", "wrong_password")
    ])
    def test_login_wrong_credentials(self, new_courier, wrong_field, value):
        payload = {"login": new_courier["login"], "password": new_courier["password"]}
        payload[wrong_field] = value
        with allure.step(f"Отправить запрос с неверным {wrong_field}"):
            response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json().get("message") == COURIER_LOGIN_NOT_FOUND

    @allure.title("Несуществующий пользователь – ошибка")
    def test_login_nonexistent_user(self):
        payload = {"login": generate_random_string(), "password": generate_random_string()}
        with allure.step("Отправить запрос с несуществующими данными"):
            response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json().get("message") == COURIER_LOGIN_NOT_FOUND