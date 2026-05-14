import allure
import requests
from data.messages import ORDER_ACCEPT_COURIER_NOT_FOUND, ORDER_ACCEPT_ORDER_NOT_FOUND
from conftest import BASE_URL

@allure.suite("Принятие заказа")
class TestAcceptOrder:

    @allure.title("Успешное принятие заказа")
    def test_accept_order_success(self, new_courier, created_order):
        courier_id = new_courier["id"]
        track = created_order
        with allure.step(f"Получить ID заказа по track {track}"):
            track_response = requests.get(f"{BASE_URL}/orders/track", params={"t": track})
            assert track_response.status_code == 200
            order_id = track_response.json()["order"]["id"]
        with allure.step(f"Принять заказ {order_id} курьером {courier_id}"):
            accept_response = requests.put(f"{BASE_URL}/orders/accept/{order_id}", params={"courierId": courier_id})
        with allure.step("Проверить код ответа и тело"):
            assert accept_response.status_code == 200
            assert accept_response.json() == {"ok": True}

    @allure.title("Принятие заказа без ID курьера – ошибка")
    def test_accept_order_no_courier_id(self, created_order):
        track = created_order
        with allure.step("Получить ID заказа по track"):
            track_response = requests.get(f"{BASE_URL}/orders/track", params={"t": track})
            assert track_response.status_code == 200
            order_id = track_response.json()["order"]["id"]
        with allure.step("Отправить запрос на принятие заказа без courierId"):
            response = requests.put(f"{BASE_URL}/orders/accept/{order_id}")
        with allure.step("Проверить код ответа (по документации 400)"):
            assert response.status_code == 400

    @allure.title("Принятие заказа с неверным ID курьера – ошибка")
    def test_accept_order_invalid_courier_id(self, created_order):
        track = created_order
        with allure.step("Получить ID заказа по track"):
            track_response = requests.get(f"{BASE_URL}/orders/track", params={"t": track})
            assert track_response.status_code == 200
            order_id = track_response.json()["order"]["id"]
        with allure.step("Отправить запрос с несуществующим courierId"):
            response = requests.put(f"{BASE_URL}/orders/accept/{order_id}", params={"courierId": 999999})
        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json().get("message") == ORDER_ACCEPT_COURIER_NOT_FOUND

    @allure.title("Принятие заказа без ID заказа – ошибка")
    def test_accept_order_no_order_id(self, new_courier):
        courier_id = new_courier["id"]
        with allure.step("Отправить запрос на принятие заказа без ID заказа"):
            response = requests.put(f"{BASE_URL}/orders/accept/", params={"courierId": courier_id})
        with allure.step("Проверить код ответа"):
            assert response.status_code == 404

    @allure.title("Принятие заказа с неверным ID заказа – ошибка")
    def test_accept_order_invalid_order_id(self, new_courier):
        courier_id = new_courier["id"]
        with allure.step("Отправить запрос с несуществующим orderId"):
            response = requests.put(f"{BASE_URL}/orders/accept/999999", params={"courierId": courier_id})
        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json().get("message") == ORDER_ACCEPT_ORDER_NOT_FOUND