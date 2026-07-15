import allure
import requests

from endpoints.endpoint import Endpoint


class PutMeme(Endpoint):
    @allure.step("Put meme")
    def put_meme(self, body, id, token=None):
        body["id"] = id
        headers = {"Authorization": token} if token else self.headers
        self.response = requests.put(
            f"{self.url}/meme/{id}",
            json=body,
            headers=headers,
        )
        if self.response.status_code == 200:
            self.json = self.response.json()
            self.post_id = self.json["id"]
        return self.response
