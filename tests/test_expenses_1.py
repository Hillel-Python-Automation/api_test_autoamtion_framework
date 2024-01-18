import random
import json
import datetime
import pytest
from src.services import ExpensesApiService

expense_api = ExpensesApiService()

@pytest.fixture(scope='module')
def create_expense_id(sign_up_response, headers, car_id):
    current_timestamp = datetime.datetime.now().isoformat()
    mileage = random.randint(2, 60000)
    payload = {
        "carId": car_id,
        "reportedAt": current_timestamp,
        "mileage": mileage,
        "liters": 11,
        "totalCost": 11,
        "forceMileage": False
    }
    response = expense_api.create_an_expense(body=json.dumps(payload), headers=headers)
    expense_id = response.get_field('data')['id']
    return expense_id
def test_create_an_expense(sign_up_response, headers, car_id):
    current_time = datetime.datetime.now().isoformat()
    mileage = random.randint(10, 900)
    liters = random.randint(5, 80)
    total = liters * 3
    payload = {
        "carId": car_id,
        "reportedAt": current_time,
        "mileage": mileage,
        "liters": liters,
        "totalCost": total,
        "forceMileage": False
    }
    response = expense_api.create_an_expense(body=json.dumps(payload), headers=headers)
    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['carId'] == payload['carId']
    assert response.get_field('data')['reportedAt'] == payload['reportedAt']
    assert response.get_field('data')['liters'] == payload['liters']
    assert response.get_field('data')['totalCost'] == payload['totalCost']
    assert response.get_field('data')['mileage'] == payload['mileage']

def test_Gets_all_expenses(sign_up_response,headers):
    response = expense_api.get_all_expenses(headers)
    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'

def test_Gets_an_expense_by_id(sign_up_response,headers,create_expense_id):
    response = expense_api.get_an_expense_by_id(headers=headers, expense_ids=create_expense_id)
    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'

def test_Edits_an_expense(sign_up_response,headers,create_expense_id,car_id):
    current_time = datetime.datetime.now().isoformat()
    mileage = random.randint(259, 900)
    liters = random.randint(5, 80)
    total_cost = liters * 3
    payload = {
        "carId": car_id,
        "reportedAt": current_time,
        "mileage": mileage,
        "liters": liters,
        "totalCost": total_cost,
        "forceMileage": False
    }
    response = expense_api.edit_an_expense(body=json.dumps(payload), headers=headers, expense_ids=create_expense_id)
    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['carId'] == payload['carId']
    assert response.get_field('data')['reportedAt'] == payload['reportedAt']
    assert response.get_field('data')['liters'] == payload['liters']
    assert response.get_field('data')['totalCost'] == payload['totalCost']
    assert response.get_field('data')['mileage'] == payload['mileage']

def test_Edits_an_expense_Copy(sign_up_response,headers,create_expense_id):
    response = expense_api.removes_an_expense(headers=headers, expense_ids=create_expense_id)
    assert response.is_status_code(200)
    assert response.get_field('status') == 'ok'
    assert int(response.get_field('data')['expenseId']) == int(create_expense_id)



