import pytest
import requests
import json
import random

@pytest.fixture(scope='module')
def sign_up_response():
    url = "https://qauto.forstudy.space/api/auth/signup"
    payload = json.dumps({
        "name": "John",
        "lastName": "Dou",
        "email": f"qweerty{random.randint(100000, 999999)}@mail.com",
        "password": "Test12341",
        "repeatPassword": "Test12341"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, timeout=5)
    return response

@pytest.fixture
def created_car_id(sign_up_response):
    url = "https://qauto.forstudy.space/api/cars"

    payload = json.dumps({
        "carBrandId": 1,
        "carModelId": 1,
        "mileage": 80000
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    return response_json['data']['id']