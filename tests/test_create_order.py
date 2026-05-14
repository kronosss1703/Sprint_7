import allure
import pytest
import requests
from data.order_data import BASE_ORDER_PAYLOAD
from conftest import BASE_URL

@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цвета")
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order_with_color(self, color):
        payload = BASE_ORDER_PAYLOAD.copy()
        payload["color"] = color
        with allure.step(f"Отправить запрос на создание заказа с цветом {color}"):
            response = requests.post(f"{BASE_URL}/orders", json=payload)
        with allure.step("Проверить код ответа и наличие track"):
            assert response.status_code == 201
            assert "track" in response.json()
            assert isinstance(response.json()["track"], int)