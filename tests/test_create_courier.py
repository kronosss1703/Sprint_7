import allure
import pytest
import requests
from conftest import generate_random_string, BASE_URL

@allure.suite("Создание курьера")
class TestCreateCourier:

    @allure.title("Курьера можно создать")
    def test_create_courier_success(self):
        login = generate_random_string()
        password = generate_random_string()
        first_name = generate_random_string()
        payload = {"login": login, "password": password, "firstName": first_name}
        response = requests.post(f"{BASE_URL}/courier", data=payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self, new_courier):
        payload = {
            "login": new_courier["login"],
            "password": new_courier["password"],
            "firstName": new_courier["firstName"]
        }
        response = requests.post(f"{BASE_URL}/courier", data=payload)
        assert response.status_code == 409
        assert response.json().get("message") == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Обязательные поля логин, пароль – без одного из них ошибка")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field(self, missing_field):
        payload = {
            "login": generate_random_string(),
            "password": generate_random_string(),
            "firstName": generate_random_string()
        }
        del payload[missing_field]
        response = requests.post(f"{BASE_URL}/courier", data=payload)
        assert response.status_code == 400
        assert response.json().get("message") == "Недостаточно данных для создания учетной записи"

    @allure.title("Создание курьера с уже существующим логином возвращает ошибку")
    def test_create_courier_existing_login_fails(self, new_courier):
        payload = {
            "login": new_courier["login"],
            "password": generate_random_string(),
            "firstName": generate_random_string()
        }
        response = requests.post(f"{BASE_URL}/courier", data=payload)
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json().get("message")