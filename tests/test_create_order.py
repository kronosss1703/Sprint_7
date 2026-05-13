import allure
import pytest
import requests
from conftest import BASE_URL

@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цвета")
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order_with_color(self, color):
        payload = {
            "firstName": "Тест",
            "lastName": "Тестов",
            "address": "Москва, ул. Тестовая, 1",
            "metroStation": 4,
            "phone": "+79991234567",
            "rentTime": 3,
            "deliveryDate": "2025-05-20",
            "comment": "Тестовый заказ",
            "color": color
        }
        response = requests.post(f"{BASE_URL}/orders", json=payload)
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)