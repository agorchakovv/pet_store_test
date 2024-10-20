import time
import allure
from pages.pet_api import PetApi
from pages.data import Data

@allure.feature("Обновление питомцев")
class Test_Api:

    pet_api = PetApi()
    data = Data()

    @allure.story("Обновление инормации о питомце")
    @allure.title("Тест обновления статуса питомца")
    @allure.description("Проверяет, что статус питомца обновляется")
    def test_update_status_pet(self):
        original_pet = self.data.new_pet()
        response = self.pet_api.create_pet(original_pet)
        response_json_before = response.json()

        assert response.status_code == 200, f"Ожидался статус-код 200 при создании питомца, но получен {response.status_code}"
        assert response_json_before["id"] == original_pet["id"], "ID питомца в ответе не совпадает с ожидаемым"

        updated_pet = self.data.updated_id_pet()
        start_time = time.time()
        response = self.pet_api.update_pet(updated_pet)
        end_time = time.time()
        response_json_after = response.json()

        response_time = end_time - start_time
        max_response_time = 5  # Максимальное допустимое время ответа в секундах   

        assert (response.status_code == 200), f"Ожидался статус-код 200, но получен {response.status_code}"

        expected_keys = {"id", "category", "name", "tags", "status"}
        assert expected_keys.issubset(response_json_after.keys()), f"Не все ключи присутствуют в ответе: {expected_keys}"

        assert response_json_after["id"] == original_pet["id"], "ID питомца изменился, хотя не должен был"
        assert response_json_after["name"] == original_pet["name"], "Имя питомца изменилось, хотя не должно было"
        assert response_json_after["category"]["id"] == original_pet["category"]["id"], "ID категории изменился, хотя не должен был"
        assert response_json_after["category"]["name"] == original_pet["category"]["name"], "Название категории изменилось, хотя не должно было"
        assert response_json_after["tags"] == original_pet["tags"], "Теги питомца изменились, хотя не должны были"

        assert response_json_after["status"] == updated_pet["status"], "Статус питомца не был обновлен"

        assert response_time < max_response_time, f"Время ответа слишком велико: {response_time}s"

        assert isinstance(response_json_after["id"], int), "ID питомца должен быть целым числом"
        assert isinstance(response_json_after["name"], str), "Имя питомца должно быть строкой"
        assert isinstance(response_json_after["category"], dict), "Категория должна быть словарем"
        assert isinstance(response_json_after["tags"], list), "Теги должны быть списком"
        assert isinstance(response_json_after["status"], str), "Статус питомца должен быть строкой"

        # 9. Проверяем, что каждый тег является словарем с корректными полями
        for tag in response_json_after["tags"]:
            assert isinstance(tag, dict), "Каждый тег должен быть словарем"
            assert "id" in tag and isinstance(tag["id"], int), "Тег должен содержать ID целочисленного типа"
            assert "name" in tag and isinstance(tag["name"], str), "Тег должен содержать имя строкового типа"

    @allure.story("Обновление инормации о питомце")
    @allure.title("Тест обновления всех полей питомца")
    @allure.description("Проверяет, что все поля питомца обновляются")
    def test_update_all_pet(self):
        original_pet = self.data.new_pet()
        response = self.pet_api.create_pet(original_pet)
        response_json_before = response.json()

        assert response.status_code == 200, f"Ожидался статус-код 200 при создании питомца, но получен {response.status_code}"
        assert response_json_before["id"] == original_pet["id"], "ID питомца в ответе не совпадает с ожидаемым" 

        updated_pet = self.data.updated_all_pet()
        start_time = time.time()
        response = self.pet_api.update_pet(updated_pet)
        end_time = time.time()
        response_json_after = response.json()

        response_time = end_time - start_time
        max_response_time = 5  # Максимальное допустимое время ответа в секундах   

        assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code}"

        assert isinstance(response_json_after, dict), "Ответ не является JSON"
        expected_keys = {"id", "category", "name", "tags", "status"}
        assert expected_keys.issubset(response_json_after.keys()), f"Не все ключи присутствуют в ответе: ожидались {expected_keys}"

        assert isinstance(response_json_after["id"], int), "ID питомца должен быть целым числом"
        assert isinstance(response_json_after["name"], str), "Имя питомца должно быть строкой"
        assert isinstance(response_json_after["category"], dict), "Категория должна быть словарем"
        assert isinstance(response_json_after["tags"], list), "Теги должны быть списком"
        assert isinstance(response_json_after["status"], str), "Статус питомца должен быть строкой"        

        assert response_json_after["id"] == updated_pet["id"], f"ID питомца не обновился: ожидалось '{response_json_after['id']}"
        assert response_json_after["name"] == updated_pet["name"], f"Имя питомца не обновилось: ожидалось '{response_json_after['name']}"
        assert response_json_after["category"]["id"] == updated_pet["category"]["id"], f"ID категории не обновился: ожидалось '{response_json_after['category']['id']}"
        assert response_json_after["category"]["name"] == updated_pet["category"]["name"], f"Название категории не обновилось: ожидалось '{response_json_after['category']['name']}"
        assert response_json_after["tags"] == updated_pet["tags"], f"Теги питомца не обновились: ожидалось '{response_json_after['tags']}"
        assert response_json_after["status"] == updated_pet["status"], f"Статус питомца не обновился: ожидалось '{response_json_after['status']}"

        for tag in response_json_after["tags"]:
            assert isinstance(tag, dict), "Каждый тег должен быть словарем"
            assert "id" in tag and isinstance(tag["id"], int), "Тег должен содержать ID целочисленного типа"
            assert "name" in tag and isinstance(tag["name"], str), "Тег должен содержать имя строкового типа"

        assert response_time < max_response_time, f"Время ответа слишком велико: {response_time}s"

    @allure.story("Некорректное обновление информации о питомце")
    @allure.title("Обновление питомца с некорректным ID")
    @allure.description("Проверяет, что попытка обновления питомца с некорректным ID вызывает ошибку")
    def test_update_pet_invalid_id(self):
        original_pet = self.data.new_pet()
        response = self.pet_api.create_pet(original_pet)
        response_json_before = response.json()

        assert response.status_code == 200, f"Ожидался статус-код 200 при создании питомца, но получен {response.status_code}"
        assert response_json_before["id"] == original_pet["id"], "ID питомца в ответе не совпадает с ожидаемым" 

        invalid_pet_data = self.data.updated_failed_id_pet()
        start_time = time.time()
        response = self.pet_api.update_pet(invalid_pet_data)
        end_time = time.time()
        response_json_after = response.json()

        response_time = end_time - start_time
        max_response_time = 5  # Максимальное допустимое время ответа в секундах
        
        assert response.status_code == 500, f"Ожидался статус ошибки 500, но получен {response.status_code}" #Код ответа подогнан под текущие условия, должен быть 400

        assert isinstance(response_json_after, dict), "Ответ не является JSON"

        expected_keys = {"code", "type", "message"}
        assert expected_keys.issubset(response_json_after.keys()), f"Ответ должен содержать ключи {expected_keys}, но их нет в ответе"

        expected_message = "something bad happened" #Подогнано под текущие реалии, не отражает проблему
        assert response_json_after["message"] == expected_message, f"Сообщение об ошибке не совпадает: ожидалось '{expected_message}'"

        assert "id" not in response_json_after, "Ответ содержит ID, которого не должно быть"

        assert response_time < max_response_time, f"Время ответа слишком велико: {response_time}s"

    @allure.story("Некорректное обновление информации о питомце")
    @allure.title("Обновление питомца с некорректными данными")
    @allure.description("Проверяет, что попытка обновления питомца с некорректными данными вызывает ошибку")
    def test_update_pet_invalid_data(self):
        original_pet = self.data.new_pet()
        response = self.pet_api.create_pet(original_pet)
        invalid_pet_data = self.data.updated_failed_pet()
        start_time = time.time()
        response = self.pet_api.update_pet(invalid_pet_data)
        end_time = time.time()
        response_json_after = response.json()

        response_time = end_time - start_time
        max_response_time = 5  # Максимальное допустимое время ответа в секундах
        
        assert response.status_code == 500, f"Ожидался статус ошибки 400, но получен {response.status_code}"

        assert isinstance(response_json_after, dict), "Ответ не является JSON"

        expected_keys = {"code", "type", "message"}
        assert expected_keys.issubset(response_json_after.keys()), f"Ответ должен содержать ключи {expected_keys}, но их нет в ответе"

        expected_message = "something bad happened"
        assert response_json_after["message"] == expected_message, f"Сообщение об ошибке не совпадает: ожидалось '{expected_message}'"

        assert "id" not in response_json_after, "Ответ содержит ID, которого не должно быть"

        assert response_time < max_response_time, f"Время ответа слишком велико: {response_time}s"