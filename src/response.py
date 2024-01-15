import logging

import allure


class AssertableResponse(object):
    def __init__(self, response):
        logging.info('Request: url={}, body={}'.format(response.request.url, response.request.body))
        logging.info('Response: status_code={}, body={}'.format(response.status_code, response.text))

        self._response = response

    @allure.step
    def is_status_code(self, code):
        logging.info('Assert: status code should be {}'.format(code))
        return self._response.status_code == code

    @allure.step
    def get_field(self, name):
        response_content_type = self._response.headers.get('content-type', '')
        if 'application/json' in response_content_type:
            return self._response.json().get(name)
        else:
            logging.warning('Response does not contain JSON content')
            return None

    @allure.step
    def get_id_by_mileage_id(self, mileage_id, field_name):
        response_content_type = self._response.headers.get('content-type', '')
        if 'application/json' in response_content_type:
            response_json = self._response.json()
            found_object = None
            for data_object in response_json["data"]:
                if data_object["mileage"] == mileage_id:
                    found_object = data_object
                    break

            assert found_object is not None, logging.warning("Object with mileage doesn't found")

            return found_object[f"{field_name}"]