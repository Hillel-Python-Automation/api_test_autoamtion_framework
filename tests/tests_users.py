import requests
import json
import random

URL = "https://qauto.forstudy.space/api"

def test_get_authenticated_user_data(sign_up_response):
    url = f"{URL}/users/current"
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("GET", url, headers=headers, timeout=5)

    assert response.status_code == 200, 'Status code broken'
    response_json = response.json()
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']

def test_get_authenticated_user_profile_data(sign_up_response):
    url = f"{URL}/users/profile"

    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("GET", url, headers=headers, timeout=5)
    response_json = response.json()
    sign_up_response_request_body = json.loads(sign_up_response.request.body)

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']
    assert response_json['data']['name'] == sign_up_response_request_body['name']
    assert response_json['data']['lastName'] == sign_up_response_request_body['lastName']


def test_gets_authenticated_user_settings_data(sign_up_response):
    url = f"{URL}/users/settings"

    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("GET", url, headers=headers)
    response_json = response.json()
    sign_up_response_request_body = json.loads(sign_up_response.request.body)

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['currency'] == sign_up_response.json()['data']['currency']
    assert response_json['data']['distanceUnits'] == sign_up_response.json()['data']['distanceUnits']

def test_edit_users_profile(sign_up_response):
    url = f"{URL}/users/profile"


    payload = json.dumps({
        "photo": "user-1621352948859.jpg",
        "name": "Test",
        "lastName": "Test",
        "dateBirth": "2021-03-17T15:21:05.000Z",
        "country": "Ukraine"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    response_json = response.json()
    sign_up_response_request_body = json.loads(sign_up_response.request.body)
    print(f"Response content: {response.text}")
    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']
    assert response_json['data']['photoFilename'] == sign_up_response.json()['data']['photoFilename']
    #assert response_json['data']['name'] == sign_up_response.json()['data']['name']
    #assert response_json['data']['lastName'] == sign_up_response.json()['data']['lastName']
    #assert response_json['data']['dateBirth'] == sign_up_response.json()['data']['dateBirth']
    #assert response_json['data']['country'] == sign_up_response.json()['data']['country']

def test_edits_users_settings(sign_up_response):
    url = f"{URL}/users/settings"

    payload = json.dumps({
        "currency": "usd",
        "distanceUnits": "km"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    response_json = response.json()
    sign_up_response_request_body = json.loads(sign_up_response.request.body)

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['currency'] == sign_up_response.json()['data']['currency']
    assert response_json['data']['distanceUnits'] == sign_up_response.json()['data']['distanceUnits']

def test_changes_users_email(sign_up_response):
    url = f"{URL}/users/email"

    payload = json.dumps({
        "email": f"qweerty{random.randint(100000, 999999)}@mail.com",
        "password": "Test12341"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    response_json = response.json()
    sign_up_response_request_body = json.loads(sign_up_response.request.body)
    print(response_json)
    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']

def test_changes_users_password(sign_up_response):
    url = f"{URL}/users/password"

    payload = json.dumps({
        "oldPassword": "Test12341",
        "password": "Test123412",
        "repeatPassword": "Test123412"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    response_json = response.json()
    sign_up_response_request_body = json.loads(sign_up_response.request.body)

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']

def test_deletes_users_account_and_current_user_session(sign_up_response):
    url = f"{URL}/users"

    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("DELETE", url, headers=headers)
    response_json = response.json()
    sign_up_response_request_body = json.loads(sign_up_response.request.body)

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
