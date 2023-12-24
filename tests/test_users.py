import requests
import json
from datetime import datetime, timezone
import random

URL = "https://qauto.forstudy.space/api"


def test_get_authenticated_user_data(sign_up_response):
    url = f"{URL}/users/current"

    payload = {}
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
    response_json = response.json()

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']


def test_get_authenticated_user_profile_data(sign_up_response):
    url = f"{URL}/users/profile"

    payload = {}
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
    response_json = response.json()
    sign_up_response_request_body = json.loads(sign_up_response.request.body)

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']
    assert response_json['data']['name'] == sign_up_response_request_body['name']
    assert response_json['data']['lastName'] == sign_up_response_request_body['lastName']


def test_edit_user_profile(sign_up_response):
    url = f"{URL}/users/profile"

    current_datetime = datetime.utcnow()
    date_birth = current_datetime.replace(tzinfo=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"

    payload = json.dumps({
        "photo": "user-1621352948859.jpg",
        "name": "Martin",
        "lastName": "Dou",
        "dateBirth": date_birth,
        "country": "Ukraine"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    response_json = response.json()
    response_date_birth = response_json['data']['dateBirth']

    assert response.status_code == 200
    assert response_json['status'] == 'ok'
    assert response_date_birth[0:19] == date_birth[0:19]


def test_edit_user_settings(sign_up_response):
    url = f"{URL}/users/settings"

    currency_codes = ["usd", "eur", "uah"]
    random_currency = random.choice(currency_codes)

    payload = json.dumps({
        "currency": random_currency,
        "distanceUnits": "km"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['data']['currency'] == random_currency
    assert response_json['data']['distanceUnits'] == payload.split()[3][1:3]


def test_change_user_email(sign_up_response):
    url = f"{URL}/users/email"

    random_email = f"qweerty{random.randint(10000, 99999)}@mail.com"

    payload = json.dumps({
        "email": random_email,
        "password": "Test12341"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']


def test_change_password(sign_up_response):
    url = f"{URL}/users/password"
    old_password = json.loads(sign_up_response.request.body)['password']

    payload = json.dumps({
        "oldPassword": old_password,
        "password": f'{old_password}+1',
        "repeatPassword": f'{old_password}+1'
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['status'] == 'ok'


def test_delete_user_account(sign_up_response):
    url = f"{URL}/users"
    # old_password = json.loads(sign_up_response.request.body)['email']

    payload = ""
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    assert response.status_code == 200
