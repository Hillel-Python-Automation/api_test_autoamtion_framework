import random
import json
from src.services import CarApiService

car_api = CarApiService()
car_id = 1


def assign_car_id(received_id):
    global car_id
    car_id = received_id


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
    assert response.status_code == 201, 'Status code broken'
    response_json = response.json()
    assign_car_id(response_json['data']['id'])
    payload_json = json.loads(payload)
    assert response_json['status'] == 'ok'
    assert response_json['data']['carBrandId'] == payload_json['carBrandId']
    assert response_json['data']['carModelId'] == payload_json['carModelId']
    assert response_json['data']['mileage'] == payload_json['mileage']


def test_gets_car_brands(sign_up_response):
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.gets_car_brands(headers=headers)
    assert response.status_code == 200, 'Status code broken'
    response_json = response.json()
    assert response_json['status'] == 'ok'
    assert response_json['data'][0]['id'] == 1
    assert response_json['data'][0]['title'] == 'Audi'
    assert response_json['data'][1]['id'] == 2
    assert response_json['data'][1]['title'] == 'BMW'
    assert response_json['data'][2]['id'] == 3
    assert response_json['data'][2]['title'] == 'Ford'
    assert response_json['data'][3]['id'] == 4
    assert response_json['data'][3]['title'] == 'Porsche'
    assert response_json['data'][4]['id'] == 5
    assert response_json['data'][4]['title'] == 'Fiat'


def test_gets_car_brands_by_id(sign_up_response):

    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.gets_car_brands_by_id(car_id=1, headers=headers)
    assert response.status_code == 200, 'Status code broken'
    response_json = response.json()
    assert response_json['status'] == 'ok'
    assert response_json['data']['id'] == 1
    assert response_json['data']['title'] == 'Audi'


def test_gets_car_models(sign_up_response):

    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.gets_car_models(headers=headers)
    assert response.status_code == 200, 'Status code broken'
    response_json = response.json()
    assert response_json['status'] == 'ok'
    assert response_json['data'][0]['id'] == 1
    assert response_json['data'][0]['title'] == 'TT'
    assert response_json['data'][1]['id'] == 2
    assert response_json['data'][1]['title'] == 'R8'
    assert response_json['data'][2]['id'] == 3
    assert response_json['data'][2]['title'] == 'Q7'
    assert response_json['data'][3]['id'] == 4
    assert response_json['data'][3]['title'] == 'A6'
    assert response_json['data'][4]['id'] == 5
    assert response_json['data'][4]['title'] == 'A8'
    assert response_json['data'][5]['id'] == 6
    assert response_json['data'][5]['title'] == '3'
    assert response_json['data'][6]['id'] == 7
    assert response_json['data'][6]['title'] == '5'
    assert response_json['data'][7]['id'] == 8
    assert response_json['data'][7]['title'] == 'X5'
    assert response_json['data'][8]['id'] == 9
    assert response_json['data'][8]['title'] == 'X6'
    assert response_json['data'][9]['id'] == 10
    assert response_json['data'][9]['title'] == 'Z3'


def test_gets_car_models_by_id(sign_up_response):

    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.gets_car_models_by_id(car_id=1, headers=headers)
    assert response.status_code == 200, 'Status code broken'
    response_json = response.json()
    assert response_json['status'] == 'ok'
    assert response_json['data']['id'] == 1
    assert response_json['data']['title'] == 'TT'


def test_gets_current_car_by_id(sign_up_response):

    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.gets_current_car_by_id(car_id, headers=headers)
    print(response.text)
    assert response.status_code == 200, 'Status code broken'
    response_json = response.json()
    assert response_json['status'] == 'ok'
    assert response_json['data']['id'] == car_id
    assert response_json['data']['brand'] == 'Audi'
    assert response_json['data']['model'] == 'TT'


def test_edits_existing_car(sign_up_response):

    payload = json.dumps({
        "carBrandId": 2,
        "carModelId": 6,
        "mileage": 168223
    })

    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.edits_existing_car(car_id, body=payload, headers=headers)
    assert response.status_code == 200, 'Status code broken'
    response_json = response.json()
    payload_json = json.loads(payload)
    assert response_json['status'] == 'ok'
    assert response_json['data']['id'] == car_id
    assert response_json['data']['carBrandId'] == payload_json['carBrandId']
    assert response_json['data']['carModelId'] == payload_json['carModelId']
    assert response_json['data']['mileage'] == payload_json['mileage']


def test_delete_existing_car(sign_up_response):

    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = car_api.delete_existing_car(car_id, headers=headers)
    assert response.status_code == 200, 'Status code broken'
    response_json = response.json()
    assert response_json['status'] == 'ok'
    assert response_json['data']['carId'] == car_id
