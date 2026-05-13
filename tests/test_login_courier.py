import allure
import pytest
import requests
from conftest import generate_random_string, BASE_URL

@allure.suite("Логин курьера")
class TestLoginCourier:

    @allure.title("Курьер может авторизоваться")
    def test_login_success(self, new_courier):
        payload = {"login": new_courier["login"], "password": new_courier["password"]}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Для авторизации нужны оба поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field(self, missing_field, new_courier):
        payload = {"login": new_courier["login"], "password": new_courier["password"]}
        del payload[missing_field]
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code != 200
        if response.status_code == 400:
            assert response.json().get("message") == "Недостаточно данных для входа"

    @allure.title("Ошибка при неверном логине или пароле")
    @pytest.mark.parametrize("wrong_field,value", [
        ("login", "wrong_login"),
        ("password", "wrong_password")
    ])
    def test_login_wrong_credentials(self, new_courier, wrong_field, value):
        payload = {"login": new_courier["login"], "password": new_courier["password"]}
        payload[wrong_field] = value
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 404
        assert response.json().get("message") == "Учетная запись не найдена"

    @allure.title("Несуществующий пользователь – ошибка")
    def test_login_nonexistent_user(self):
        payload = {"login": generate_random_string(), "password": generate_random_string()}
        response = requests.post(f"{BASE_URL}/courier/login", data=payload)
        assert response.status_code == 404
        assert response.json().get("message") == "Учетная запись не найдена"