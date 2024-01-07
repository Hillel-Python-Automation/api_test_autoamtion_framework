import random
import json

import pytest
from _pytest.fixtures import fixture

from src.services import CarApiService

car_api = CarApiService()


def print_steps(response):
    print('\n' + '-' * 60)
    print(f"Steps:")
    print(f"1) Send the request:")
    print(f"Method:\t{response.request.method} {response.request.url}")
    if response.request.body:
        print(f"Body:\n{json.dumps(json.loads(response.request.body), indent=2)}")
    print('-' * 60)
    print(f"Actual Result:")
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    print('-' * 60)


@fixture(scope="module")
def create_new_car(sign_up_response):
    payload = json.dumps({
        "carBrandId": 1,
        "carModelId": 1,
        "mileage": 0
    })

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.create_new_car(body=payload, headers=headers)

    return response


def test_01_create_new_car(sign_up_response, create_new_car):
    response = create_new_car
    print_steps(response=response)

    assert response.status_code == 201, 'Status code broken'
    response_json = response.json()
    assert response_json['status'] == 'ok'
    assert response_json['data']['carBrandId'] == json.loads(response.request.body)['carBrandId']
    assert response_json['data']['carModelId'] == json.loads(response.request.body)['carModelId']
    assert response_json['data']['mileage'] == json.loads(response.request.body)['mileage']


@fixture(scope="module")
def get_car_brands(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.get_car_brands(headers=headers)

    return response


def test_02_get_car_brands(get_car_brands):
    response = get_car_brands
    response_json = response.json()
    print_steps(response=response)

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data'][0]['id'] == 1
    assert response_json['data'][0]['title'] == "Audi"
    assert response_json['data'][0]['logoFilename'] == 'audi.png'


@pytest.mark.parametrize('brand_id', list(range(0, 7)))
def test_03_get_car_brand_by_id(sign_up_response, get_car_brands, brand_id):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.get_car_brand_by_id(headers=headers, brand_id=brand_id)
    print_steps(response=response)
    if brand_id > 5 or brand_id < 1:
        assert response.status_code == 404
        assert response.json()['status'] == 'error'
        assert response.json()['message'] == 'No car brands found with this id'
    else:
        assert response.status_code == 200, 'Status code broken'
        response_json = response.json()
        get_car_brands_json = get_car_brands.json()
        assert response_json['status'] == 'ok'
        assert response_json['data'] == get_car_brands_json['data'][brand_id - 1]


@fixture(scope="module")
def get_car_models(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.get_car_models(headers=headers)

    return response


def test_04_get_car_models(get_car_models):
    response = get_car_models
    response_json = response.json()
    print_steps(response=response)

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data'][0]['id'] == 1
    assert response_json['data'][0]['carBrandId'] == 1
    assert response_json['data'][0]['title'] == 'TT'


@pytest.mark.parametrize('model_id', list(range(0, 25)))
def test_05_get_car_brand_by_id(sign_up_response, get_car_models, model_id):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.get_car_model_by_id(headers=headers, model_id=model_id)
    print_steps(response=response)
    if model_id > 23 or model_id < 1:
        assert response.status_code == 404
        assert response.json()['status'] == 'error'
        assert response.json()['message'] == 'No car models found with this id'
    else:
        assert response.status_code == 200, 'Status code broken'
        response_json = response.json()
        get_car_models_json = get_car_models.json()
        assert response_json['status'] == 'ok'
        assert response_json['data'] == get_car_models_json['data'][model_id - 1]


@pytest.mark.xfail(reason='updatedMileageAt and carCreatedAt timestamp returns without milliseconds - .000z')
def test_06_get_current_user_car_id_by_id(sign_up_response, create_new_car):
    created_car = create_new_car.json()['data']

    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }
    response = car_api.get_current_user_car_by_id(headers=headers, car_id=created_car['id'])
    print_steps(response=response)
    response_json = response.json()

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['id'] == created_car['id']
    assert response_json['data']['carBrandId'] == created_car['carBrandId']
    # assert response_json['data'] == created_car


def test_07_edit_existing_car(sign_up_response, create_new_car, get_car_models):
    created_car = create_new_car.json()['data']

    random_car_brand = random.randint(1, 6)
    random_car_model = random.choice(
        [item['id'] for item in get_car_models.json()['data'] if item['carBrandId'] == random_car_brand])

    payload = json.dumps({
        "carBrandId": random_car_brand,
        "carModelId": random_car_model,
        "mileage": random.randint(created_car['mileage'], 999999 + 1)
    })

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.edit_existing_car(body=payload, headers=headers, car_id=created_car['id'])
    print_steps(response=response)

    assert response.status_code == 200, 'Status code broken'
    response_json = response.json()
    assert response_json['status'] == 'ok'
    assert response_json['data']['carBrandId'] == json.loads(payload)['carBrandId']
    assert response_json['data']['carModelId'] == json.loads(payload)['carModelId']
    assert response_json['data']['mileage'] == json.loads(payload)['mileage']


def test_08_delete_existing_car(sign_up_response, create_new_car):
    created_car = create_new_car.json()['data']

    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.delete_existing_car(headers=headers, car_id=created_car['id'])
    response_json = response.json()
    print_steps(response=response)

    assert response.status_code == 200, 'Status code broken'
    assert response_json['data']['carId'] == created_car['id']
