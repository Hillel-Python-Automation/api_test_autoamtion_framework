import random
import json
from src.services import UserApiService

user_api = UserApiService()


def test_gets_authenticated_user_settings_data(sign_up_response, headers):
    response = user_api.get_user_settings(headers=headers)

    assert response.is_status_code(200)
    assert response.get_field("status") == "ok"
    assert response.get_field("data")["currency"] == "usd"
    assert response.get_field("data")["distanceUnits"] == "km"


def test_edit_user_profile(sign_up_response, headers):
    body = json.dumps({
        "name": "John",
        "lastName": "Dou",
        "dateBirth": "2021-03-17T15:21:05.000Z",
        "country": "Ukraine"})
    headers['Content-Type'] = 'application/json'

    response = user_api.edit_user_profile(body=body, headers=headers)
    payload_json = json.loads(body)
    sign_up_response_request_body = json.loads(sign_up_response.request.body)

    assert response.is_status_code(200)
    assert response.get_field("status") == "ok"
    assert response.get_field("data")["userId"] == \
           sign_up_response.json()["data"]["userId"]
    assert response.get_field("data")["photoFilename"] == \
           sign_up_response.json()["data"]["photoFilename"]
    assert response.get_field("data")["name"] == sign_up_response_request_body[
        "name"]
    assert response.get_field("data")["lastName"] == \
           sign_up_response_request_body["lastName"]
    assert response.get_field("data")["country"] == "Ukraine"


def test_get_users_settings(sign_up_response, headers):
    response = user_api.get_user_settings(headers=headers)
    sign_up_response = sign_up_response.json()

    assert response.is_status_code(200)
    assert response.get_field("status") == "ok"
    assert response.get_field("data")["distanceUnits"] == \
           sign_up_response["data"]["distanceUnits"]
    assert response.get_field("data")["currency"] == sign_up_response["data"][
        "currency"]


def test_changes_users_email(sign_up_response, headers):
    sign_up_response_request_body = json.loads(sign_up_response.request.body)
    body = json.dumps({
        "email": f"test{random.randint(10000000, 99999999)}katehonchar@gmsil.com",
        "password": sign_up_response_request_body["password"]
    })
    response = user_api.change_user_email(body=body, headers=headers)

    assert response.is_status_code(200)
    assert response.get_field("status") == "ok"
    assert response.get_field("data")["userId"] == \
           sign_up_response.json()["data"]["userId"]


def test_changes_users_password(sign_up_response, headers):
    sign_up_response_request_body = json.loads(sign_up_response.request.body)
    old_password = sign_up_response_request_body["password"]
    new_password = "123" + old_password
    body = json.dumps({
        "oldPassword": f"{old_password}",
        "password": f"{new_password}",
        "repeatPassword": f"{new_password}"
    })
    headers['Content-Type'] = 'application/json'
    response = user_api.change_user_password(body=body, headers=headers)

    assert response.is_status_code(200)
    assert response.get_field("status") == "ok"
    assert response.get_field("data")["userId"] == \
           sign_up_response.json()["data"]["userId"]


def test_deletes_users_account_and_current_user_session(sign_up_response,
                                                        headers):
    response = user_api.delete_user(headers=headers)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
