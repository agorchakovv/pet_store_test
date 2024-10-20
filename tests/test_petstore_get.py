import time
import allure
from pages.pet_api import PetApi
from pages.data import Data

@allure.feature("Получение питомцев по ID")
class Test_Api:

    pet_api = PetApi()
    data = Data()

    @allure.story("Получение питомца по ID")
    @allure.title("Тест успешного получения питомца по ID")
    @allure.description("Проверяет, что питомец приходит в ответе по ID")
    def test_get_pet_by_id_success(self):
        pet = self.data.new_pet()
        response = self.pet_api.create_pet(pet)
        response_json_before = response.json()

        assert response.status_code == 200, f"Ожидался статус-код 200 при создании питомца, но получен {response.status_code}"
        assert response_json_before["id"] == pet["id"], "ID питомца в ответе не совпадает с ожидаемым"


        start_time = time.time()
        response = self.pet_api.get_pet_by_id(pet["id"])
        end_time = time.time()
        response_json = response.json()

        response_time = end_time - start_time
        max_response_time = 5  # Максимальное допустимое время ответа в секундах        

        assert (response.status_code == 200), f"Ожидался статус 200, но получен {response.status_code}"

        assert isinstance(response_json, dict), "Ответ не является JSON"

        expected_keys = {"id", "category", "name", "tags", "status"}
        assert expected_keys.issubset(response_json.keys()), f"Не все ключи присутствуют в ответе: ожидались {expected_keys}"     

        assert isinstance(response_json["id"], int), "ID питомца должен быть целым числом"
        assert isinstance(response_json["name"], str), "Имя питомца должно быть строкой"
        assert isinstance(response_json["category"], dict), "Категория должна быть словарем"
        assert isinstance(response_json["tags"], list), "Теги должны быть списком"
        assert isinstance(response_json["status"], str), "Статус питомца должен быть строкой"          

        for tag in response_json["tags"]:
            assert isinstance(tag, dict), "Каждый тег должен быть словарем"
            assert "id" in tag and isinstance(tag["id"], int), "Тег должен содержать ID целочисленного типа"
            assert "name" in tag and isinstance(tag["name"], str), "Тег должен содержать имя строкового типа"   

        assert response_json["tags"] == pet["tags"], "Теги питомца не совпадают"          

        assert response_json["id"] == pet["id"], "ID питомца не совпадает"

        assert (response_json["name"] == pet["name"]), f"Имя питомца не совпадает: ожидалось '{pet['name']}', но получено '{response_json['name']}'"

        assert (response_json["category"]["id"] == pet["category"]["id"]), "ID категории не совпадает"
        assert (response_json["category"]["name"] == pet["category"]["name"]), "Название категории не совпадает"

        assert (response_json["status"] == pet["status"]), f"Статус питомца не совпадает: ожидалось {response_json['status']}"

        assert (response_time < max_response_time), f"Время ответа слишком велико: {response_time}s"

    @allure.story("Получение питомца по ID")
    @allure.title("Тест отсутствия получения питомца по некорректному ID")
    @allure.description("Проверяет, что питомец не приходит в ответе по некорректному ID")
    def test_get_pet_by_id_not_found(self):
        non_existent_pet_id = 999999999
        start_time = time.time()
        response = self.pet_api.get_pet_by_id(non_existent_pet_id)
        end_time = time.time()
        response_json = response.json()

        response_time = end_time - start_time
        max_response_time = 5  # Максимальное допустимое время ответа в секундах        

        assert (response.status_code == 404), f"Ожидался статус-код 404, но получен {response.status_code}"

        assert isinstance(response_json, dict), "Ответ не является JSON"

        expected_keys = {"code", "type", "message"}
        assert expected_keys.issubset(response_json.keys()), f"Ожидались ключи {expected_keys}, но в ответе их нет"        

        assert "message" in response_json, "Ответ не содержит ключа 'message'"

        expected_message = "Pet not found"
        assert (response_json["message"] == expected_message), f"Сообщение об ошибке не совпадает: ожидалось {response_json['message']}"

        assert "id" not in response_json, "Ответ содержит id, которого не должно быть"

        assert (response_json.get("code") == 1), f"Ожидался код ошибки 1, но получено {response_json.get('code')}"

        assert (response_time < max_response_time), f"Время ответа слишком велико: {response_time}s"