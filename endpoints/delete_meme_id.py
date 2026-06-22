import requests
from endpoints.endpoint import Endpoint
import allure


class DeleteMeme(Endpoint):
    @allure.step('Delete meme by id')
    def delete_meme(self, id, token=None):
        headers = {"Authorization": token} if token else self.headers
        self.response = requests.delete(
            f'{self.url}/meme/{id}',
            headers=headers,
        )
        return self.response

    @allure.step('Check delete success message')
    def check_delete_message(self, expected_id):
        expected_text = f"Meme with id {expected_id} successfully deleted"

        assert self.response.text == expected_text, \
            f"Ожидался текст '{expected_text}',"\
            "но получен '{self.response.text}'"
