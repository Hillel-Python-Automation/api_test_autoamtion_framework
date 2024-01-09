import json
from api_test_autoamtion_framework.src.services import CarApiService

car_api = CarApiService()


def test_create_new_car(sign_up_response):
    payload = json.dumps({
        "carBrandId": 1,
        "carModelId": 1,
        "mileage": 1
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }
    response = car_api.create_new_car(body=payload, headers=headers)

    if response.status_code != 201:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response text: {response.text}")
    response_json = response.json()
    payload_json = json.loads(payload)
    assert response.status_code == 201
    assert response_json['data']['carBrandId'] == payload_json['carBrandId']
    assert response_json['data']['carModelId'] == payload_json['carModelId']
    assert response_json['data']['mileage'] == payload_json['mileage']
    car_id = response_json['data']['id']
    return car_id


def test_get_car_brands(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }
    response = car_api.get_car_brands(headers=headers)
    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response text: {response.text}")
    assert response.status_code == 200, 'OK'


def test_get_car_brand_by_id(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }
    response = car_api.get_car_brand_by_id(headers=headers)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['data']['id'] == 1
    assert response_json['data']['title'] == 'Audi'


def test_get_car_models(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }
    response = car_api.get_cars_models(headers=headers)
    assert response.status_code == 200


def test_get_cars_model_by_id(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }
    response = car_api.get_car_model_by_id(headers=headers)
    assert response.status_code == 200


def test_get_current_user_cars(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }
    response = car_api.get_current_user_cars(headers=headers)
    assert response.status_code == 200


def test_get_current_user_car_by_id(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }
    created_car_id = test_create_new_car(sign_up_response)
    response = car_api.get_current_user_car_by_id(headers=headers, car_id=created_car_id)
    assert response.status_code == 200


def test_edit_existing_car_by_id(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "carBrandId": 1,
        "carModelId": 1,
        "mileage": 168223
    })
    created_car_id = test_create_new_car(sign_up_response)
    response = car_api.edit_existing_car_by_id(headers=headers, body=payload, car_id=created_car_id)
    response_json = response.json()
    pay_load = json.loads(payload)
    assert response_json['status'] == 'ok'
    assert response_json['data']['carBrandId'] == pay_load['carBrandId']
    assert response_json['data']['carModelId'] == pay_load['carModelId']
    assert response_json['data']['mileage'] == pay_load['mileage']


def test_delete_existing_car(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }
    created_car_id = test_create_new_car(sign_up_response)
    response = car_api.delete_existing_car(headers=headers, car_id=created_car_id)
    assert response.status_code == 200
