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
