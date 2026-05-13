import allure
import requests
from conftest import register_new_courier, delete_courier, BASE_URL

@allure.suite("Удаление курьера")
class TestDeleteCourier:

    @allure.title("Успешное удаление курьера")
    def test_delete_courier_success(self):
        courier = register_new_courier()
        assert courier is not None
        courier_id = courier["id"]
        response = requests.delete(f"{BASE_URL}/courier/{courier_id}")
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Удаление без ID курьера – ошибка")
    def test_delete_courier_no_id(self):
        response = requests.delete(f"{BASE_URL}/courier/")
        assert response.status_code == 404

    @allure.title("Удаление с несуществующим ID – ошибка")
    def test_delete_courier_invalid_id(self):
        response = requests.delete(f"{BASE_URL}/courier/999999")
        assert response.status_code == 404
        assert "Курьера с таким id нет" in response.json().get("message", "")