import requests
from endpoints.endpoint import Endpoint
import allure


class PutMeme(Endpoint):
    @allure.step('Put meme')
    def put_meme(self, body, id, token=None):
        body['id'] = id
        headers = {"Authorization": token} if token else self.headers
        self.response = requests.put(
            f'{self.url}/meme/{id}',
            json=body,
            headers=headers,
        )
        if self.response.status_code == 200:
            self.json = self.response.json()
            self.post_id = self.json['id']
        return self.response

    @allure.step('Check update meme fields match body and user')
    def check_update_meme_fields(self, expected_body, expected_user):
        assert self.json.get('text') == expected_body['text'], \
            f"Ожидался текст '{expected_body['text']}',"\
            "получен '{self.json.get('text')}'"

        assert self.json.get('url') == expected_body['url'], \
            f"Ожидался url '{expected_body['url']}',"\
            "получен '{self.json.get('url')}'"

        assert self.json.get('tags') == expected_body['tags'], \
            f"Ожидались теги {expected_body['tags']},"\
            "получены {self.json.get('tags')}"

        assert self.json.get('info') == expected_body['info'], \
            f"Ожидалось инфо {expected_body['info']},"\
            "получено {self.json.get('info')}"

        assert self.json.get('id') == str(expected_body['id']), \
            f"Ожидалось инфо {str(expected_body['id'])},"\
            "получено {self.json.get('id')}"

        assert self.json.get('updated_by') == expected_user, \
            f"Ожидался автор '{expected_user}',"\
            "получен '{self.json.get('updated_by')}'"
