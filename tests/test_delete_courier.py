import allure
import requests
from helpers.courier_api import register_new_courier
from data.messages import COURIER_DELETE_NOT_FOUND
from conftest import BASE_URL

@allure.suite("Удаление курьера")
class TestDeleteCourier:

    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self):
        courier = register_new_courier()
        assert courier is not None
        courier_id = courier["id"]
        with allure.step(f"Отправить запрос на удаление курьера {courier_id}"):
            response = requests.delete(f"{BASE_URL}/courier/{courier_id}")
        with allure.step("Проверить код ответа и тело"):
            assert response.status_code == 200
            assert response.json() == {"ok": True}

    @allure.title("Удаление без ID курьера – ошибка")
    def test_delete_courier_no_id(self):
        with allure.step("Отправить запрос на удаление без указания ID"):
            response = requests.delete(f"{BASE_URL}/courier/")
        with allure.step("Проверить код ответа"):
            assert response.status_code == 404

    @allure.title("Удаление с несуществующим ID – ошибка")
    def test_delete_courier_invalid_id(self):
        with allure.step("Отправить запрос на удаление с несуществующим ID"):
            response = requests.delete(f"{BASE_URL}/courier/999999")
        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 404
            assert COURIER_DELETE_NOT_FOUND in response.json().get("message", "")