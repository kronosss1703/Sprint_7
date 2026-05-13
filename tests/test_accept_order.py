import allure
import requests
from conftest import BASE_URL

@allure.suite("Принятие заказа")
class TestAcceptOrder:

    @allure.title("Успешное принятие заказа")
    def test_accept_order_success(self, new_courier, created_order):
        courier_id = new_courier["id"]
        track = created_order
        track_response = requests.get(f"{BASE_URL}/orders/track", params={"t": track})
        assert track_response.status_code == 200
        order_id = track_response.json()["order"]["id"]
        accept_response = requests.put(f"{BASE_URL}/orders/accept/{order_id}", params={"courierId": courier_id})
        assert accept_response.status_code == 200
        assert accept_response.json() == {"ok": True}

    @allure.title("Принятие заказа без ID курьера – ошибка")
    def test_accept_order_no_courier_id(self, created_order):
        track = created_order
        track_response = requests.get(f"{BASE_URL}/orders/track", params={"t": track})
        order_id = track_response.json()["order"]["id"]
        response = requests.put(f"{BASE_URL}/orders/accept/{order_id}")
        assert response.status_code in (400, 404)

    @allure.title("Принятие заказа с неверным ID курьера – ошибка")
    def test_accept_order_invalid_courier_id(self, created_order):
        track = created_order
        track_response = requests.get(f"{BASE_URL}/orders/track", params={"t": track})
        order_id = track_response.json()["order"]["id"]
        response = requests.put(f"{BASE_URL}/orders/accept/{order_id}", params={"courierId": 999999})
        assert response.status_code == 404
        assert "Курьера с таким id не существует" in response.json().get("message", "")

    @allure.title("Принятие заказа без ID заказа – ошибка")
    def test_accept_order_no_order_id(self, new_courier):
        courier_id = new_courier["id"]
        response = requests.put(f"{BASE_URL}/orders/accept/", params={"courierId": courier_id})
        assert response.status_code == 404

    @allure.title("Принятие заказа с неверным ID заказа – ошибка")
    def test_accept_order_invalid_order_id(self, new_courier):
        courier_id = new_courier["id"]
        response = requests.put(f"{BASE_URL}/orders/accept/999999", params={"courierId": courier_id})
        assert response.status_code == 404
        assert "Заказа с таким id не существует" in response.json().get("message", "")