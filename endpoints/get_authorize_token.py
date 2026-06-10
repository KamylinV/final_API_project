import requests
from endpoints.endpoint import Endpoint
import allure


class CheckAuthorezeToken(Endpoint):
    @allure.step('Check token')
    def check_token(self, token):
        self.response = requests.get(f'{self.url}/authorize/{token}')

        if self.response.status_code == 200:
            self.json = self.response.text
            self.token_alive = token
        return self.response
