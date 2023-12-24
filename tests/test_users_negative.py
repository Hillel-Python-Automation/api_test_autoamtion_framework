import requests
import json
import random

URL = "https://qauto.forstudy.space/api"


def test_get_authenticated_user_data_without_cookie(sign_up_response):
    url = f"{URL}/users/current"

    payload = {}
    headers = {
        'Cookie': None
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
    response_json = response.json()

    assert response.status_code == 401, 'Not authenticated'
    assert response_json['status'] == 'error'


def test_change_password_to_the_same(sign_up_response):
    url = f"{URL}/users/password"
    old_password = json.loads(sign_up_response.request.body)['password']

    payload = json.dumps({
        "oldPassword": old_password,
        "password": old_password,
        "repeatPassword": old_password
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    response_json = response.json()
    print(response.text)
    assert response.status_code == 400, 'New password should not be the same'
    assert response_json['status'] == 'error'


def test_change_user_invalid_email(sign_up_response):
    url = f"{URL}/users/email"

    random_email = f"qweerty{random.randint(10000, 99999)}mail.com"

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

    assert response.status_code == 400
    assert response_json['status'] == 'error', 'Email is incorrect'
