import requests
from endpoints.endpoint import Endpoint
import allure


class GetAllMeme(Endpoint):
    @allure.step('Get all meme')
    def get_all_meme(self, token=None):
        headers = {"Authorization": token} if token else self.headers
        self.response = requests.get(
            f'{self.url}/meme',
            headers=headers,
        )
        if self.response.status_code == 200:
            self.json = self.response.json()
        return self.response
