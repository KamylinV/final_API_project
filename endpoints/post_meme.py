import allure
import requests

from endpoints.endpoint import Endpoint


class PostMeme(Endpoint):
    @allure.step("Post meme")
    def post_meme(self, body, token=None):
        headers = {"Authorization": token} if token else self.headers
        self.response = requests.post(
            f"{self.url}/meme",
            json=body,
            headers=headers,
        )
        if self.response.status_code == 200:
            self.json = self.response.json()
            self.post_id = self.json["id"]
        return self.response
