import requests
from endpoints.endpoint import Endpoint
import allure


class GetMemeId(Endpoint):
    @allure.step('Gettind one meme by ID')
    def get_one_meme(self, id, token):
        headers = {"Authorization": token} if token else self.headers
        self.response = requests.get(
            f'{self.url}/meme/{id}',
            headers=headers
        )
        if self.response.status_code == 200:
            self.json = self.response.json()
        return self.response

    @allure.step('Check id')
    def check_id(self, expected_id):
        assert self.json.get('id') == expected_id, \
            f"Ожидался id = {expected_id}, получен {self.json.get('id')}"
