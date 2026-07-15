import pytest

test_data = [{"name": "Bober"}]

invalid_payload_data = [
    {"text": "Meme without image url", "tags": ["invalid"], "info": {"Ya": "Good bay"}},
    {
        "text": "Yandex taxi",
        "url": "https://memepedia.ru/glavnye-memy-yanvarya-2026/",
        "tags": ["I go to the taxi"],
    },
    {
        "url": "https://memepedia.ru/glavnye-memy-yanvarya-2026/",
        "tags": ["I go to the taxi"],
        "info": {"Ya": "Go"},
    },
    {
        "text": "Yandex taxi",
        "url": "https://memepedia.ru/glavnye-memy-yanvarya-2026/",
        "info": {"Ya": "Go"},
    },
]


@pytest.mark.parametrize("data", test_data)
def test_get_token_for_user(post_authorize, data):
    post_authorize.post_authorize_get_token(data)
    post_authorize.check_status_code(200)
    post_authorize.check_response_name(data["name"])


def test_token_alive(token_alive, auth_token):
    token_alive.check_token(auth_token["token"])
    token_alive.check_status_code(200)


def test_token_alive_negative(token_alive, auth_token):
    token_alive.check_token(auth_token["token"] + "1")
    token_alive.check_status_code(404)


def test_get_all_meme_success(all_meme, auth_token):
    all_meme.get_all_meme(token=auth_token["token"])
    all_meme.check_status_code(200)
    all_meme.check_memes_list_is_not_empty()


def test_get_all_memes_without_token(all_meme):
    all_meme.get_all_meme()
    all_meme.check_status_code(401)


def test_create_meme_success(
    post_new_meme, auth_token, yandex_taxi_payload, delete_meme_endpoint
):
    post_new_meme.post_meme(body=yandex_taxi_payload, token=auth_token["token"])
    post_new_meme.check_status_code(200)
    post_new_meme.check_meme_fields(
        expected_body=yandex_taxi_payload, expected_user=auth_token["user"]
    )
    created_id = post_new_meme.post_id
    delete_meme_endpoint.delete_meme(id=created_id, token=auth_token["token"])


@pytest.mark.parametrize("data", invalid_payload_data)
def test_create_meme_with_missing_required_fields(data, post_new_meme, auth_token):
    post_new_meme.post_meme(body=data, token=auth_token["token"])
    post_new_meme.check_status_code(400)


def test_get_one_meme(created_meme_id, get_meme_id, auth_token):
    get_meme_id.get_one_meme(id=created_meme_id, token=auth_token["token"])
    get_meme_id.check_status_code(200)
    get_meme_id.check_id(expected_id=created_meme_id)


def test_get_one_meme_invalid_id(get_meme_id, auth_token):
    get_meme_id.get_one_meme(id="not_a_number", token=auth_token["token"])
    get_meme_id.check_status_code(404)


def test_update_meme(
    created_meme_id,
    auth_token,
    updated_meme_payload,
    updated_meme,
):
    updated_meme.put_meme(
        body=updated_meme_payload, id=created_meme_id, token=auth_token["token"]
    )
    updated_meme.check_status_code(200)
    updated_meme.check_meme_fields(
        expected_body=updated_meme_payload, expected_user=auth_token["user"]
    )


def test_update_meme_without_token(updated_meme, created_meme_id, updated_meme_payload):
    updated_meme.put_meme(body=updated_meme_payload, id=created_meme_id, token=None)
    updated_meme.check_status_code(401)


def test_delete_meme_success(
    created_meme_id, delete_meme_endpoint, auth_token, get_meme_id
):
    delete_meme_endpoint.delete_meme(id=created_meme_id, token=auth_token["token"])
    meme_id = created_meme_id
    delete_meme_endpoint.check_status_code(200)
    delete_meme_endpoint.check_delete_message(expected_id=meme_id)
    get_meme_id.get_one_meme(id=meme_id, token=auth_token["token"])
    get_meme_id.check_status_code(404)


def test_delete_meme_twice(created_meme_id, delete_meme_endpoint, auth_token):
    delete_meme_endpoint.delete_meme(id=created_meme_id, token=auth_token["token"])
    delete_meme_endpoint.check_status_code(200)
    delete_meme_endpoint.delete_meme(id=created_meme_id, token=auth_token["token"])
    delete_meme_endpoint.check_status_code(404)
