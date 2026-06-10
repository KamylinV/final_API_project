import allure


class Endpoint:
    def __init__(self):
        self.response = None
        self.url = 'http://memesapi.course.qa-practice.com'
        self.headers = {'Content-Type': 'application/json'}

    @allure.step('Check that status code is {expected_code}')
    def check_status_code(self, expected_code=200):
        assert self.response.status_code == expected_code, \
            f"Ожидался код {expected_code}, получен {self.response.status_code}"

    @allure.step('Check that user = name')
    def check_response_name(self, name):
        assert self.response.json().get('user') == name, \
            f"Ожидается имя {name}, получен {self.response.json().get('user')}"

    # @allure.step('Check that data is updated')
    # def check_update_data(self, name):
    #     assert self.response.json()['name'] == name
