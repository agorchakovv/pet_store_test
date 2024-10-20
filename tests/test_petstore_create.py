import time
import allure
from pages.pet_api import PetApi
from pages.data import Data

@allure.feature("Создание питомцев")
class Test_Api:

    pet_api = PetApi()
    data = Data()

    @allure.story("Создание питомца")
    @allure.title("Тест успешного создания питомца")
    @allure.description("Проверяет успешное создание питомца с корректными данными.")
    def test_create_pet_success(self):
        pet = self.data.new_pet()
        start_time = time.time()
        response = self.pet_api.create_pet(pet)
        end_time = time.time()
        response_json = response.json()

        response_time = end_time - start_time
        max_response_time = 5  # Максимальное допустимое время ответа в секундах

        assert response.status_code == 200, "Неверный статус-код при создании питомца"

        assert isinstance(response_json, dict), "Ответ не является JSON"

        expected_keys = {"id", "category", "name", "tags", "status"}
        assert expected_keys.issubset(response_json.keys()), "Не все ключи присутствуют в ответе"        

        assert response_json["id"] == pet["id"], "ID питомца не совпадает"

        assert response_json["name"] == pet["name"], "Имя питомца не совпадает"

        assert (response_json["category"]["id"] == pet["category"]["id"]), "ID категории не совпадает"
        assert (response_json["category"]["name"] == pet["category"]["name"]), "Название категории не совпадает"

        assert response_json["tags"] == pet["tags"], "Теги питомца не совпадают"

        assert response_json["status"] == pet["status"], "Статус питомца не совпадает"

        assert (response_time < max_response_time), f"Время ответа слишком велико: {response_time}s"

    @allure.story("Создание питомца")
    @allure.title("Тест некорректного создания питомца")
    @allure.description("Проверяет, что питомец не создается с некорректными данными")
    def test_create_pet_unsuccessful_id(self):
        pet = self.data.new_pet_invalid_data_id()
        start_time = time.time()
        response = self.pet_api.create_pet(pet)
        end_time = time.time()
        response_json = response.json()

        response_time = end_time - start_time
        max_response_time = 5  # Максимальное допустимое время ответа в секундах  

        assert response.status_code == 500, "Неверный статус-код ошибки"

        response_json = response.json()
        assert isinstance(response_json, dict), "Ответ не является JSON"

        expected_keys = {"code", "type", "message"}
        assert expected_keys.issubset(response_json.keys()), f"Не все ключи присутствуют в ответе: ожидались {expected_keys}"        

        assert "message" in response_json, "Ответ не содержит ключа 'message'"

        expected_message = "something bad happened"
        assert response_json["message"] == expected_message, f"Сообщение об ошибке не совпадает: ожидалось {response_json['message']}"

        assert "id" not in response_json, "Ответ не содержит id, которого не должно быть"

        pet["name"] = ""
        response_empty_name = self.pet_api.create_pet(pet)
        assert response_empty_name.status_code == 500, "Неверный статус-код ошибки"

        pet.pop("name")  
        response_no_name = self.pet_api.create_pet(pet)
        assert response_no_name.status_code == 500, "Неверный статус-код ошибки"     

        assert (response_time < max_response_time), f"Время ответа слишком велико: {response_time}s"


    @allure.step("Пустое имя")
    @allure.title("Тест некорректного создания питомца с пустым именем")
    @allure.description("Проверяет, что питомец не создается с пустым именем")    
    def test_create_pet_unsuccessful_name_missing(self):
        pet = self.data.new_pet_invalid_data_id()
        response_empty_name = self.pet_api.create_pet(pet)

        assert response_empty_name.status_code == 500, "Неверный статус-код ошибки"

    @allure.step("Без имени")
    @allure.title("Тест некорректного создания питомца без имени")
    @allure.description("Проверяет, что питомец не создается без имени")
    def test_create_pet_unsuccessful_name_empty(self):
        pet = self.data.new_pet_invalid_data_id()
        pet.pop("name")  
        response_no_name = self.pet_api.create_pet(pet)

        assert response_no_name.status_code == 500, "Неверный статус-код ошибки"   