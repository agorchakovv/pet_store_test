import requests
from utils.config import BasePage


class PetApi(BasePage):

    def create_pet(self, pet_data):
        """Создать нового питомца"""
        response = requests.post(self.api_url(), json=pet_data)
        return response

    def get_pet_by_id(self, pet_id):
        """Получить питомца по ID"""
        response = requests.get(f"{self.api_url()}/{pet_id}")
        return response

    def update_pet(self, pet_data):
        """Обновить данные о питомце"""
        response = requests.put(self.api_url(), json=pet_data)
        return response

    def delete_pet(self, pet_id):
        """Удалить питомца по ID"""
        response = requests.delete(f"{self.api_url()}/{pet_id}")
        return response
