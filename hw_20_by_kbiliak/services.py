import random

import allure
import requests

from src.services import ApiService
from src.response import AssertableResponse


class CarApiService(ApiService):
    def __init__(self):
        super().__init__()

    @allure.step
    def post_new_car(self, body, headers):
        headers['Content-Type'] = 'application/json'
        return AssertableResponse(
            self._post(endpoint="/cars", body=body, headers=headers))

    @allure.step
    def gets_car_brands(self, headers):
        return AssertableResponse(
            self._get(endpoint="/cars/brands", headers=headers))

    @allure.step
    def gets_car_brand_by_id(self, headers, random):
        return AssertableResponse(
            self._get(endpoint=f"/cars/brands/{random}",
                      headers=headers))

    @allure.step
    def gets_car_models(self, headers):
        return AssertableResponse(
            self._get(endpoint="/cars/models", headers=headers))

    @allure.step
    def gets_car_model_by_id(self, headers, random):
        return AssertableResponse(
            self._get(endpoint=f"/cars/models/{random}",
                                      headers=headers))

    @allure.step
    def gets_current_user_car_by_id(self, headers, created_car_id):
        return AssertableResponse(
            self._get(endpoint=f"/cars/{created_car_id}",
                                             headers=headers))

    @allure.step
    def edits_existing_car(self, headers, body, created_car_id):
        return AssertableResponse(
            self._put(endpoint=f"/cars/{created_car_id}", body=body,
                                    headers=headers))

    @allure.step
    def deletes_existing_car(self, headers, created_car_id):
        return AssertableResponse(
            self._delete(endpoint=f"/cars/{created_car_id}",
                                      headers=headers))
