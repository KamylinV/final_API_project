import requests
from endpoints.endpoint import Endpoint
import allure


class PostAuthorize(Endpoint):
    @allure.step('Get token')
    def post_authorize_get_token(self, body, headers=None):
        headers = headers if headers else self.headers
        self.response = requests.post(
            f'{self.url}/authorize',
            json=body,
            headers=headers,
        )
        if self.response.status_code == 200:
            self.json = self.response.json()
            self.token = self.json.get('token')
            self.user = self.json.get('user')
        return self.response
