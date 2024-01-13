import random
import json
import datetime

import pytest
from _pytest.fixtures import fixture

from src.services import ExpensesApiService
from tests.conftest import sign_up_response, headers

exp_api = ExpensesApiService()


@fixture()
def create_an_expense(headers, car_data):
    payload = json.dumps({
        "carId": car_data['id'],
        "reportedAt": (datetime.datetime.strptime(car_data['carCreatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ') +
                       datetime.timedelta(microseconds=1)).strftime("%Y-%m-%d"),
        "mileage": car_data['initialMileage'] + 1,
        "liters": 11.0,
        "totalCost": 11.0,
        "forceMileage": False,
    })
    response = exp_api.create_an_expense(body=payload, headers=headers)
    return response


def get_all_expenses_ids_all_pages(headers, carId):
    all_ids = []
    total_items = exp_api.get_all_expenses(headers=headers, page=0, carId=carId).get_field('totalItems')
    for i in range(1, int(total_items / 10) + 2):
        current_page = exp_api.get_all_expenses(headers=headers, page=i, carId=carId)
        ids_on_page = [page['id'] for page in current_page.get_field('data')]
        all_ids.extend(ids_on_page)
    return all_ids


def test_01_create_an_expense(headers, create_an_expense):
    response = create_an_expense
    created_id = response.get_field('data')['id']
    created_expense_carId = response.get_field('data')['carId']
    assert response.get_field('status') == 'ok'
    assert created_expense_carId == json.loads(response.get_request_body())['carId']
    assert response.get_field('data')['reportedAt'] == json.loads(response.get_request_body())['reportedAt']
    assert response.get_field('data')['liters'] == json.loads(response.get_request_body())['liters']
    assert isinstance(created_id, int)
    assert response.get_field('data')['mileage'] == json.loads(response.get_request_body())['mileage']
    assert response.get_field('data')['totalCost'] == json.loads(response.get_request_body())['totalCost']
    assert created_id in get_all_expenses_ids_all_pages(headers=headers, carId=created_expense_carId)


@fixture
def get_all_expenses(headers):
    response = exp_api.get_all_expenses(headers=headers, page=None, carId=None)
    return response


@pytest.mark.xfail(reason='''Bugs:
1) liters and totalCost properties are int but they should be float.
2) page and carId parameters are marked as required, but they are not required''')
def test_02_get_all_expenses(get_all_expenses):
    assert get_all_expenses.get_field('status') == 'ok'
    for item in get_all_expenses.get_field('data'):
        assert isinstance(item['id'], int)
        assert isinstance(item['carId'], int)
        assert isinstance(item['reportedAt'], str)
        assert isinstance(item['mileage'], int)
        # assert isinstance(item['liters'], float)
        # assert isinstance(item['totalCost'], float)


def test_03_get_an_expense_by_id(headers, create_an_expense):
    expense_id = create_an_expense.get_field('data')['id']
    response = exp_api.get_an_expense_by_id(headers=headers, expenseId=expense_id)

    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['id'] == expense_id
    assert response.get_field('data')['carId'] == create_an_expense.get_field('data')['carId']
    assert response.get_field('data')['reportedAt'] == create_an_expense.get_field('data')['reportedAt']
    assert response.get_field('data')['mileage'] == create_an_expense.get_field('data')['mileage']
    assert response.get_field('data')['liters'] == create_an_expense.get_field('data')['liters']
    assert response.get_field('data')['totalCost'] == create_an_expense.get_field('data')['totalCost']


def test_03_2_get_an_expense_by_id__random_from_the_list(headers, get_all_expenses):
    all_expense_ids = [i['id'] for i in get_all_expenses.get_field('data')]
    random_index = random.randint(0, len(all_expense_ids))
    expense_id = all_expense_ids[random_index]

    response = exp_api.get_an_expense_by_id(headers=headers, expenseId=expense_id)

    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['id'] == expense_id


@pytest.mark.xfail(reason='''Bugs: 
1) id is returned as a string, but should be int''')
def test_04_edit_an_expense_by_id(headers, create_an_expense):
    expense_id = create_an_expense.get_field('data')['id']

    payload = json.dumps({
        "carId": create_an_expense.get_field('data')['carId'],
        "reportedAt": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
        "mileage": create_an_expense.get_field('data')['mileage'] + 1,
        "liters": 11.0,
        "totalCost": 11.0,
        "forceMileage": False,
    })

    response = exp_api.edit_an_expense(headers=headers, body=payload, expenseId=expense_id)

    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['carId'] == json.loads(payload)['carId']
    assert response.get_field('data')['reportedAt'] == json.loads(payload)['reportedAt']
    # assert response.get_field('data')['id'] == expense_id
    assert response.get_field('data')['mileage'] == json.loads(payload)['mileage']
    assert response.get_field('data')['totalCost'] == json.loads(payload)['totalCost']


def test_05_delete_an_expense(headers, create_an_expense):
    expense_id = create_an_expense.get_field('data')['id']
    response = exp_api.delete_an_expense(headers=headers, expenseId=expense_id)

    assert response.get_field('status') == 'ok'
    assert response.get_field('data')['expenseId'] == str(expense_id)
