import allure
import requests

from endpoints.endpoint import Endpoint


class GetAllMeme(Endpoint):
    @allure.step("Get all meme")
    def get_all_meme(self, token=None):
        headers = {"Authorization": token} if token else self.headers
        self.response = requests.get(
            f"{self.url}/meme",
            headers=headers,
        )
        if self.response.status_code == 200:
            self.json = self.response.json()
        return self.response

    @allure.step("Check that memes list is not empty")
    def check_memes_list_is_not_empty(self):
        memes_list = self.json.get("data", [])

        assert isinstance(memes_list, list), (
            "Поле 'data' в ответе сервера не является списком!"
        )

        assert len(memes_list) > 0, "Список мемов на сервере пуст!"
