import datetime
import random
import string

import requests
import json

URL = "https://qauto.forstudy.space/api"


def test_get_authenticated_user_data(sign_up_response):
    url = f"{URL}/users/current"

    payload = {}
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=5)

    assert response.status_code == 200, 'Status code broken'
    response_json = response.json()
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


def test_03_gets_authenticated_user_settings_data(sign_up_response):
    url = f"{URL}/users/settings"

    payload = {}
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
    response_json = response.json()
    sign_up_response_content = json.loads(sign_up_response.content)

    assert response.status_code == 200
    assert response_json['status'] == 'ok'
    assert response_json['data']['currency'] == sign_up_response_content['data']['currency']
    assert response_json['data']['distanceUnits'] == sign_up_response_content['data']['distanceUnits']


def print_execution_steps(response):
    print(f'''
Steps:
1) Send {response.request.method} request to {response.request.url}
with payload:
{json.dumps(json.loads(response.request.body), indent=2)}

Actual Result:
Status code = {response.status_code}
{json.dumps(response.json(), indent=2)}
    ''')


def test_04_edit_users_profile(sign_up_response):
    url = f"{URL}/users/profile"

    payload = json.dumps({
        "photo": f"user-1621352{random.randint(100000, 999999)}.jpg",
        "name": f"Test{''.join(random.choices(string.ascii_lowercase, k=6))}",
        "lastName": f"Test{''.join(random.choices(string.ascii_lowercase, k=6))}",
        "dateBirth": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-7] + "000Z",
        # "2021-03-17T15:21:05.000Z",
        "country": random.choice(["Ukraine", "United States", "United Kingdom", "Poland", "Canada"])
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, timeout=5)
    response_json = response.json()
    sign_up_response_content = json.loads(sign_up_response.content)
    payload_json = json.loads(payload)
    print_execution_steps(response=response)

    assert response.status_code == 200
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response_content['data']['userId']
    # Bug? photoFilename returns always "photoFilename": "default-user.png" value?
    assert response_json['data']['photoFilename'] == payload_json['photo']
    # Bug? Not possible to enter special chars and digits
    assert response_json['data']['name'] == payload_json['name']
    assert response_json['data']['lastName'] == payload_json['lastName']
    # Bug? dateBirth returns hours, mins, and seconds
    assert response_json['data']['dateBirth'] == payload_json['dateBirth']
    assert response_json['data']['country'] == payload_json['country']


def test_05_edit_users_settings(sign_up_response):
    url = f"{URL}/users/settings"

    payload = json.dumps({
        "currency": random.choice(["eur", "gbp", "usd", "uah", "pln"]),
        "distanceUnits": random.choice(["km", "ml"])
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, timeout=5)
    response_json = response.json()
    payload_json = json.loads(payload)
    print_execution_steps(response=response)

    assert response.status_code == 200
    assert response_json['status'] == 'ok'
    assert response_json['data']['currency'] == payload_json['currency']
    assert response_json['data']['distanceUnits'] == payload_json['distanceUnits']


def test_06_changes_users_email(sign_up_response):
    url = f"{URL}/users/email"

    payload = json.dumps({
        "email": f"qweerty{random.randint(100000, 999999)}@mail.com",
        "password": json.loads(sign_up_response.request.body)['password']
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, timeout=5)
    response_json = response.json()
    sign_up_response_content = json.loads(sign_up_response.content)

    assert response.status_code == 200
    assert response_json['status'] == 'ok'
    # Why the response does not contain new email?
    # assert response_json['data']['email'] == payload_json['email']
    assert response_json['data']['userId'] == sign_up_response_content['data']['userId']


def generate_new_password():
    password = (random.choices(string.ascii_lowercase) +
                random.choices(string.ascii_uppercase) +
                random.choices(string.digits) +
                random.choices(string.printable, k=random.randint(8 - 3, 15 - 3)))

    random.shuffle(password)
    return ''.join(password)


def test_07_changes_users_password(sign_up_response):
    url = f"{URL}/users/password"

    new_pass = generate_new_password()
    print(new_pass)

    payload = json.dumps({
        "oldPassword": json.loads(sign_up_response.request.body)['password'],
        "password": new_pass,
        "repeatPassword": new_pass,
    })
    headers = {

        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload, timeout=5)
    response_json = response.json()
    sign_up_response_content = json.loads(sign_up_response.content)

    assert response.status_code == 200
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response_content['data']['userId']


def test_08_deletes_users_account_and_current_user_session(sign_up_response):
    url = f"{URL}/users"

    payload = ""
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload, timeout=5)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['status'] == 'ok'


def test_08_2_deletes_users_account_and_current_user_session___not_authenticated():
    url = f"{URL}/users"

    payload = ""
    headers = {
        'Cookie': 'sid=some_fake_cookies'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload, timeout=5)
    response_json = response.json()

    assert response.status_code == 401
    assert response_json['status'] == 'error'
    assert response_json['message'] == 'Not authenticated'
