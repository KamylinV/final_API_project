import pytest
import os
from endpoints.post_authorize import PostAuthorize
from endpoints.get_authorize_token import CheckAuthorezeToken


TOKEN_FILE = ".token.txt"


@pytest.fixture()
def post_authorize():
    return PostAuthorize()


@pytest.fixture()
def token_alive():
    return CheckAuthorezeToken()


@pytest.fixture()
def auth_token():
    checker = CheckAuthorezeToken()
    authorizer = PostAuthorize()

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            saved_token = file.read().strip()

        if saved_token:
            checker.check_token(saved_token)
            if checker.response.status_code == 200:
                return saved_token
    authorizer.post_authorize_get_token(body={"name": "Bober23"})
    new_token = authorizer.token

    if not new_token:
        pytest.fail("Не удалось сгенерировать токен!")

    with open(TOKEN_FILE, "w") as file:
        file.write(new_token)

    return new_token
