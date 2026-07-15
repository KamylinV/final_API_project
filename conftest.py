import os

import pytest

import data
from endpoints.delete_meme_id import DeleteMeme
from endpoints.get_authorize_token import CheckAuthorizeToken
from endpoints.get_meme import GetAllMeme
from endpoints.get_meme_id import GetMemeId
from endpoints.post_authorize import PostAuthorize
from endpoints.post_meme import PostMeme
from endpoints.put_meme_id import PutMeme

TOKEN_FILE = ".token.txt"


@pytest.fixture()
def post_authorize():
    return PostAuthorize()


@pytest.fixture()
def token_alive():
    return CheckAuthorizeToken()


@pytest.fixture(scope="session")
def auth_token():
    checker = CheckAuthorizeToken()
    authorizer = PostAuthorize()

    default_username = data.DEFAULT_USERNAME

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            saved_token = file.read().strip()

        if saved_token:
            checker.check_token(saved_token)
            if checker.response.status_code == 200:
                return {"token": saved_token, "user": default_username}
    authorizer.post_authorize_get_token(body={"name": default_username})
    new_token = authorizer.token

    if not new_token:
        pytest.fail("Не удалось сгенерировать токен!")

    with open(TOKEN_FILE, "w") as file:
        file.write(new_token)

    return {"token": new_token, "user": default_username}


@pytest.fixture()
def all_meme():
    return GetAllMeme()


@pytest.fixture()
def get_meme_id():
    return GetMemeId()


@pytest.fixture()
def post_new_meme():
    return PostMeme()


@pytest.fixture()
def yandex_taxi_payload():
    return data.YANDEX_TAXI_PAYLOAD


@pytest.fixture()
def created_meme_id(
    post_new_meme, auth_token, yandex_taxi_payload, delete_meme_endpoint
):
    post_new_meme.post_meme(body=yandex_taxi_payload, token=auth_token["token"])
    meme_id = post_new_meme.post_id
    yield meme_id

    print(f"\n[Cleanup] Автоматически удаляем созданный мем с ID: {meme_id}")
    delete_meme_endpoint.delete_meme(id=meme_id, token=auth_token["token"])


@pytest.fixture()
def updated_meme_payload():
    return data.UPDATED_MEME_PAYLOAD


@pytest.fixture()
def updated_meme():
    return PutMeme()


@pytest.fixture()
def delete_meme_endpoint():
    return DeleteMeme()


@pytest.fixture()
def clean_meme(post_new_meme, delete_meme_endpoint, auth_token):
    yield

    if hasattr(post_new_meme, "post_id") and post_new_meme.post_id:
        meme_id = post_new_meme.post_id
        print(f"\n[Cleanup] Автоматически удаляемсозданный тест-мем с ID: {{meme_id}}")

        delete_meme_endpoint.delete_meme(id=meme_id, token=auth_token["token"])
