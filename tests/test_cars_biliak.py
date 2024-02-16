import json
import random

from src.biliak_services import CarApiService
car_api = CarApiService()
import pytest


def test_creates_new_car(headers):
    body = json.dumps({
      "carBrandId": 1,
      "carModelId": 1,
      "mileage": 1
    })
    response = car_api.post_new_car(body=body, headers=headers)

    assert response.is_status_code(201)
    assert response.get_field("status") == "ok"
    assert response.get_field("data")["id"] is not None
    assert response.get_field("data")["carBrandId"] == 1
    assert response.get_field("data")["brand"] == "Audi"


def test_gets_car_brands(headers):
    response = car_api.gets_car_brands(headers=headers)

    assert response.is_status_code(200)
    assert response.get_field("status") == "ok"
    assert response.get_field("data")[0]["id"] == 1
    assert response.get_field("data")[0]["title"] == "Audi"
    assert response.get_field("data")[0]["logoFilename"] == "audi.png"

def test_gets_car_brand_by_id(headers):
    id_generator = random.randint(1, 5)
    response = car_api.gets_car_brand_by_id(headers=headers, random=id_generator )

    assert response.is_status_code(200)
    assert response.get_field("status") == "ok"
    assert response.get_field("data")["id"] == id_generator


def test_gets_car_models(headers):
    response = car_api.gets_car_models(headers=headers)
    cars = response.get_field("data")
    car = cars[0]

    assert response.is_status_code(200)
    assert response.get_field("status") == "ok"
    assert len(cars) > 0
    assert car["id"] == 1
    assert car["title"] == "TT"

def test_gets_car_model_by_id(headers):
    car_id = random.randint(1, 23)
    response = car_api.gets_car_model_by_id(headers=headers, random=car_id)

    assert response.is_status_code(200)
    assert response.get_field("status") == "ok"
    assert response.get_field("data")["id"] == car_id


def test_gets_current_user_car_by_id(headers, new_car):
    response = car_api.gets_current_user_car_by_id(headers=headers, created_car_id=new_car['id'])

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'


def test_edits_existing_car(headers, new_car):
    expected_mileage = random.randint(0, 10000)
    body = json.dumps({
        "carBrandId": 1,
        "carModelId": 2,
        "mileage": expected_mileage
    })

    response = car_api.edits_existing_car(body=body, headers=headers, created_car_id=new_car["id"])

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['mileage'] == expected_mileage


def test_deletes_existing_car(headers, new_car):
    deleted_response = car_api.deletes_existing_car(headers=headers, created_car_id=new_car["id"])
    assert deleted_response.is_status_code(200)
    assert deleted_response.get_field('status') == 'ok'

    get_response = car_api.gets_current_user_car_by_id(headers=headers, created_car_id=new_car["id"])
    assert get_response.is_status_code(404)
    assert get_response.get_field("status") == "error"
