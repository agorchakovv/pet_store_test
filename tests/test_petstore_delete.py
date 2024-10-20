import time
import allure
from pages.pet_api import PetApi
from pages.data import Data

@allure.feature("Удаление питомцев")
class Test_Api:

    pet_api = PetApi()
    data = Data()
      

    @allure.story("Удаление питомца")
    @allure.title("Удаление существующего питомца")
    @allure.description("Проверяет, что питомец корректно удаляется")
    def test_delete_pet_success(self):
        original_pet = self.data.new_pet()
        response = self.pet_api.create_pet(original_pet)
        response_json_before = response.json()

        assert response.status_code == 200, f"Ожидался статус-код 200 при создании питомца, но получен {response.status_code}"
        assert response_json_before["id"] == original_pet["id"], "ID питомца в ответе не совпадает с ожидаемым"
        
        pet_id = response_json_before["id"]

        start_time = time.time()
        response = self.pet_api.delete_pet(pet_id)
        end_time = time.time()

        response_time = end_time - start_time
        max_response_time = 5  # Максимальное допустимое время ответа в секундах

        assert response.status_code == 200, f"Ожидался статус-код 200 при удалении питомца, но получен {response.status_code}"

        response_after_delete = self.pet_api.get_pet_by_id(pet_id)
        
        assert response_after_delete.status_code == 404, f"Ожидался статус-код 404 для запроса удаленного питомца, но получен {response_after_delete.status_code}"
        
        response_json_after_delete = response_after_delete.json()

        expected_message = "Pet not found"
        assert response_json_after_delete.get("message") == expected_message, f"Сообщение об ошибке не совпадает: ожидалось '{expected_message}'"

        assert "id" not in response_json_after_delete, "Ответ не должен содержать 'id' для удаленного питомца"

        assert response_time < max_response_time, f"Время ответа слишком велико: {response_time}s"

    @allure.story("Удаление питомца")
    @allure.title("Попытка удаления несуществующего питомца")
    @allure.description("Проверяет, что при попытке удалить несуществующего питомца возвращается корректная ошибка")
    def test_delete_nonexistent_pet(self):

        nonexistent_pet_id = 999999999  

        start_time = time.time()
        response = self.pet_api.delete_pet(nonexistent_pet_id)
        end_time = time.time()

        response_time = end_time - start_time
        max_response_time = 5  # Максимальное допустимое время ответа в секундах

        assert response.status_code == 404, f"Ожидался статус-код 404, но получен {response.status_code}"

        assert response_time < max_response_time, f"Время ответа слишком велико: {response_time}s"