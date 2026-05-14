import allure
import requests
from conftest import BASE_URL

@allure.suite("Список заказов")
class TestOrdersList:

    @allure.title("Тело ответа содержит список заказов")
    def test_orders_list_is_list(self):
        with allure.step("Отправить запрос на получение списка заказов"):
            response = requests.get(f"{BASE_URL}/orders")
        with allure.step("Проверить код ответа и структуру"):
            assert response.status_code == 200
            assert isinstance(response.json(), dict)
            assert "orders" in response.json()
            assert isinstance(response.json()["orders"], list)