import os
import allure
import requests
from src.response import AssertableResponse

class ApiService(object):
    def __init__(self):
        self._base_url = os.environ['BASE_URL']
class ExpensesApiService(ApiService):
    def __init__(self):
        super().__init__()

    @allure.step('GET: {endpoint}')
    def _get(self, endpoint, headers):
        return requests.get(f"{self._base_url}{endpoint}", headers=headers)

    @allure.step('POST: {endpoint}')
    def _post(self, endpoint, body, headers):
        headers['Content-Type'] = 'application/json'
        return requests.post(f"{self._base_url}{endpoint}", data=body,
                             headers=headers)

    @allure.step('PUT: {endpoint}')
    def _put(self, endpoint, body, headers):
        headers['Content-Type'] = 'application/json'
        return requests.put(f"{self._base_url}{endpoint}", data=body,
                            headers=headers)

    @allure.step('DELETE: {endpoint}')
    def _delete(self, endpoint, headers):
        return requests.delete(f"{self._base_url}{endpoint}", headers=headers)

    @allure.step
    def create_an_expense(self, headers, body):
        return AssertableResponse(
            self._post(endpoint="/expenses", body=body, headers=headers))

    @allure.step
    def gets_all_expenses(self, headers):
        return AssertableResponse(self._get(endpoint="/expenses", headers=headers))

    @allure.step
    def gets_an_expense_by_id(self, headers, expense_ids):
        return AssertableResponse(self._get(endpoint=f"/expenses/{expense_ids}", headers=headers))

    @allure.step
    def edits_an_expense(self, headers, body, expense_ids):
        return AssertableResponse(self._put(endpoint=f"/expenses/{expense_ids}", body=body, headers=headers))

    @allure.step
    def delete_an_expense(self, headers, expense_ids):
        return AssertableResponse(self._delete(endpoint=f"/expenses/{expense_ids}", headers=headers))
