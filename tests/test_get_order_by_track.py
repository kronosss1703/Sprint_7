import allure
import requests
from conftest import BASE_URL

@allure.suite("Получение заказа по номеру")
class TestGetOrderByTrack:

    @allure.title("Успешное получение заказа по track")
    def test_get_order_by_track_success(self, created_order):
        track = created_order
        response = requests.get(f"{BASE_URL}/orders/track", params={"t": track})
        assert response.status_code == 200
        assert "order" in response.json()
        assert response.json()["order"]["track"] == track

    @allure.title("Запрос без номера заказа – ошибка")
    def test_get_order_no_track(self):
        response = requests.get(f"{BASE_URL}/orders/track")
        assert response.status_code == 400
        assert response.json().get("message") == "Недостаточно данных для поиска"

    @allure.title("Запрос с несуществующим track – ошибка")
    def test_get_order_invalid_track(self):
        response = requests.get(f"{BASE_URL}/orders/track", params={"t": 999999999})
        assert response.status_code == 404
        assert response.json().get("message") == "Заказ не найден"