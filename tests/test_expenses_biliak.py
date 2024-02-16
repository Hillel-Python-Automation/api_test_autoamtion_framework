import pytest
import random
import json
import datetime
from src.biliak_services import ExpensesApiService

expense_api = ExpensesApiService()


@pytest.fixture(scope='module')
def create_expense_by_id(headers, car_id):
    current_timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=3)
    mileage = random.randint(2, 13)
    body = {
        "carId": car_id,
        "reportedAt": current_timestamp.isoformat(),
        "mileage": mileage,
        "liters": 11,
        "totalCost": 11,
        "forceMileage": False
    }
    response = expense_api.create_an_expense(body=json.dumps(body),
                                             headers=headers)
    expense_id = response.get_field("data")["id"]
    return expense_id


def test_create_an_expense(headers, car_id):
    current_timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=3)
    body = {
        "carId": car_id,
        "reportedAt": current_timestamp.isoformat(),
        "mileage": 12,
        "liters": 15,
        "totalCost": 45,
        "forceMileage": False
    }
    response = expense_api.create_an_expense(body=json.dumps(body),
                                             headers=headers)
    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['reportedAt'] == body['reportedAt']
    assert response.get_field('data')['mileage'] == 12
    assert response.get_field('data')['liters'] == 15
    assert response.get_field('data')['totalCost'] == 45


def test_gets_all_expenses(headers):
    response = expense_api.gets_all_expenses(headers)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')[0]['id'] is not None
    assert response.get_field('data')[0]['totalCost'] > 0


def test_gets_an_expense_by_id(headers, create_expense_by_id):
    response = expense_api.gets_an_expense_by_id(headers=headers,
                                                expense_ids=create_expense_by_id)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['liters'] is not None
    assert response.get_field('data')["totalCost"] > 0


def test_edits_an_expense(sign_up_response, headers, car_id,
                          create_expense_by_id):
    current_timestamp = datetime.datetime.now().isoformat()

    body = {
        "carId": car_id,
        "reportedAt": current_timestamp,
        "mileage": 500,
        "liters": 30,
        "totalCost": 90,
        "forceMileage": False
    }
    response = expense_api.edits_an_expense(body=json.dumps(body),
                                           headers=headers,
                                           expense_ids=create_expense_by_id)
    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['reportedAt'] == body['reportedAt']
    assert response.get_field('data')['mileage'] == 500
    assert response.get_field('data')['liters'] == 30
    assert response.get_field('data')['totalCost'] == 90
    assert response.get_field('data')['carId'] == body['carId']


def test_edits_an_expense_copy(headers, create_expense_by_id):
    response = expense_api.delete_an_expense(headers=headers,
                                              expense_ids=create_expense_by_id)

    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert int(response.get_field('data')['expenseId']) == create_expense_by_id
