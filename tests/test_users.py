import random
import json

from src.services import UserApiService

user_api = UserApiService()


def test_get_authenticated_user_data(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = user_api.get_user_current(headers=headers)

    assert response.status_code == 200, 'Status code broken'
    response_json = response.json()
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']


def test_get_authenticated_user_profile_data(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = user_api.get_user_profile(headers=headers)
    response_json = response.json()
    sign_up_response_request_body = json.loads(sign_up_response.request.body)

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']
    assert response_json['data']['name'] == sign_up_response_request_body['name']
    assert response_json['data']['lastName'] == sign_up_response_request_body['lastName']


def test_get_authenticated_user_settings_data(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = user_api.get_user_settings(headers=headers)
    response_json = response.json()

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['currency'] == sign_up_response.json()['data']['currency']
    assert response_json['data']['distanceUnits'] == sign_up_response.json()['data']['distanceUnits']


def test_edit_user_profile(sign_up_response):
    payload = json.dumps({
        "photo": "user-1621352948859.jpg",
        "name": "John",
        "lastName": "Dou",
        "dateBirth": "2021-03-17T15:21:05.000Z",
        "country": "Ukraine"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = user_api.edit_user_profile(body=payload, headers=headers)
    response_json = response.json()
    payload_json = json.loads(payload)
    sign_up_response_request_body = json.loads(sign_up_response.request.body)

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']
    assert response_json['data']['photoFilename'] == sign_up_response.json()['data']['photoFilename']
    assert response_json['data']['name'] == sign_up_response_request_body['name']
    assert response_json['data']['lastName'] == sign_up_response_request_body['lastName']
    assert response_json['data']['dateBirth'] == payload_json['dateBirth']
    assert response_json['data']['country'] == payload_json['country']


def test_edits_users_settings(sign_up_response):
    payload = json.dumps({
        "currency": "usd",
        "distanceUnits": "km"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = user_api.edit_user_settings(body=payload, headers=headers)
    response_json = response.json()
    payload_json = json.loads(payload)

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['currency'] == payload_json['currency']
    assert response_json['data']['distanceUnits'] == payload_json['distanceUnits']


def test_changes_users_email(sign_up_response):
    sign_up_response_request_body = json.loads(sign_up_response.request.body)
    password_value = sign_up_response_request_body['password']
    payload = json.dumps({
        "email": f"qweerty{random.randint(10000000, 99999999)}@mail.com",
        "password": f"{password_value}"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = user_api.change_user_email(body=payload, headers=headers)
    response_json = response.json()

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']


def test_changes_users_password(url, sign_up_response):
    sign_up_response_request_body = json.loads(sign_up_response.request.body)
    password_value = sign_up_response_request_body['password']
    new_password_value = 'new' + password_value

    payload = json.dumps({
        "oldPassword": f"{password_value}",
        "password": f"{new_password_value}",
        "repeatPassword": f"{new_password_value}"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = user_api.change_user_password(body=payload, headers=headers)
    response_json = response.json()

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']


def test_delete_users_account_and_session(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = user_api.delete_user(headers=headers)
    response_json = response.json()

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'