import allure


class Endpoint:
    def __init__(self):
        self.response = None
        self.url = "http://memesapi.course.qa-practice.com"
        self.headers = {"Content-Type": "application/json"}

    @allure.step("Check that status code is {expected_code}")
    def check_status_code(self, expected_code=200):
        assert self.response.status_code == expected_code, (
            f"Ожидался код {expected_code},получен {self.response.status_code}"
        )

    @allure.step("Check that user = name")
    def check_response_name(self, name):
        assert self.response.json().get("user") == name, (
            f"Ожидается имя {name},получен {self.response.json().get('user')}"
        )

    @allure.step("Check meme fields match expected data")
    def check_meme_fields(self, expected_body, expected_user):
        assert self.json.get("text") == expected_body["text"], (
            f"Ожидался текст '{expected_body['text']}', получен '{self.json.get('text')}'"
        )

        assert self.json.get("url") == expected_body["url"], (
            f"Ожидался url '{expected_body['url']}', получен '{self.json.get('url')}'"
        )

        assert self.json.get("tags") == expected_body["tags"], (
            f"Ожидались теги {expected_body['tags']}, получены {self.json.get('tags')}"
        )

        assert self.json.get("info") == expected_body["info"], (
            f"Ожидалось инфо {expected_body['info']}, получено {self.json.get('info')}"
        )

        assert self.json.get("updated_by") == expected_user, (
            f"Ожидался автор '{expected_user}', получен '{self.json.get('updated_by')}'"
        )
