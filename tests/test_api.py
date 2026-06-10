import pytest


test_data = [{"name": "Bober"}]


@pytest.mark.parametrize('data', test_data)
def test_get_toren_for_user(post_authorize, data):
    post_authorize.post_authorize_get_token(data)
    post_authorize.check_status_code(200)
    post_authorize.check_response_name(data["name"])


def test_token_alive(token_alive, auth_token):
    token_alive.check_token(auth_token)
    token_alive.check_status_code(200)


def test_token_alive_negative(token_alive, auth_token):
    token_alive.check_token(auth_token + '1')
    token_alive.check_status_code(404)
