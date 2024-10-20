class Data:

    def new_pet(self):

        data = {
            "id": 1,
            "category": {"id": 1, "name": "sosiska"},
            "name": "sosisochka",
            "tags": [{"id": 1, "name": "minidog"}],
            "status": "available",
        }

        return data

    def new_pet_invalid_data_id(self):

        data = {
            "id": "asd",
            "category": {"id": 1, "name": "sosiska"},
            "name": "sosisochka",
            "tags": [{"id": 1, "name": "minidog"}],
            "status": "available",
        }

        return data
    
    def updated_id_pet(self):

        data = {
            "id": 1,
            "category": {"id": 1, "name": "sosiska"},
            "name": "sosisochka",
            "tags": [{"id": 1, "name": "minidog"}],
            "status": "in_good_hand",
        }

        return data    
    
    def updated_all_pet(self):

        data = {
            "id": 1,
            "category": {"id": 2, "name": "ne_sosiska"},
            "name": "ne_sosisochka",
            "tags": [{"id": 2, "name": "big_dog"}],
            "status": "not_exist",
        }

        return data      
    
    def updated_failed_pet(self):

        data = {
            "id": "odin",
            "category": {"id": 2, "name": 123},
            "name": "",
            "tags": "dog",
            "status": "999",
        }

        return data      

    def updated_failed_id_pet(self):

        data = {
            "id": "dva",
            "category": {"id": 1, "name": "sosiska"},
            "name": "sosisochka",
            "tags": [{"id": 1, "name": "minidog"}],
            "status": "available",
        }

        return data        