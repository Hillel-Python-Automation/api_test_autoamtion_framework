import os
import pytest
import requests
import json
import random

from src.services import CarApiService

car_api = CarApiService()


@pytest.fixture(scope='session')
def sign_up_response(url):
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
    response = requests.request("POST", f"{url}/auth/signup", headers=headers, data=payload, timeout=5)
    return response


@pytest.fixture(scope='session')
def headers(sign_up_response):
    return {'Cookie': f'sid={sign_up_response.cookies.get("sid")}'}


@pytest.fixture(scope='session')
def url():
    return os.environ['BASE_URL']


@pytest.fixture()
def get_cars_models(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = CarApiService().get_cars_model(headers=headers)

    return response


@pytest.fixture()
def car_data(sign_up_response, headers, get_cars_models):
    random_car_brand = random.randint(1, 6)
    random_car_model = random.choice(
        [item['id'] for item in get_cars_models.get_field('data') if item['carBrandId'] == random_car_brand])

    payload = json.dumps({
        "carBrandId": random_car_brand,
        "carModelId": random_car_model,
        "mileage": 1
    })
    headers['Content-Type'] = 'application/json'
    response = car_api.create_new_car(body=payload, headers=headers)
    return response.get_field('data')
