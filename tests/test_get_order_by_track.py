import allure
import requests
from data.messages import ORDER_GET_BY_TRACK_MISSING, ORDER_GET_BY_TRACK_NOT_FOUND
from conftest import BASE_URL

@allure.suite("Получение заказа по номеру")
class TestGetOrderByTrack:

    @allure.title("Успешное получение заказа по track")
    def test_get_order_by_track_success(self, created_order):
        track = created_order
        with allure.step(f"Отправить запрос на получение заказа по track {track}"):
            response = requests.get(f"{BASE_URL}/orders/track", params={"t": track})
        with allure.step("Проверить код ответа и содержимое"):
            assert response.status_code == 200
            assert "order" in response.json()
            assert response.json()["order"]["track"] == track

    @allure.title("Запрос без номера заказа – ошибка")
    def test_get_order_no_track(self):
        with allure.step("Отправить запрос без параметра t"):
            response = requests.get(f"{BASE_URL}/orders/track")
        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json().get("message") == ORDER_GET_BY_TRACK_MISSING

    @allure.title("Запрос с несуществующим track – ошибка")
    def test_get_order_invalid_track(self):
        with allure.step("Отправить запрос с несуществующим track"):
            response = requests.get(f"{BASE_URL}/orders/track", params={"t": 999999999})
        with allure.step("Проверить код ответа и сообщение об ошибке"):
            assert response.status_code == 404
            assert response.json().get("message") == ORDER_GET_BY_TRACK_NOT_FOUND