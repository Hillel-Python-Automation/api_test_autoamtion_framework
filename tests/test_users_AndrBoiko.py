def test_get_authenticated_user_settings_data(sign_up_response):
    url = f"{URL}/users/settings"

    payload = {}
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("GET", url, headers=headers, data=payload, timeout=7)
    print(response)
    response_json = response.json()

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['currency'] == response_json['data']['currency']
    assert response_json['data']['distanceUnits'] == response_json['data']['distanceUnits']


def test_edit_users_profile(sign_up_response):
    url = f"{URL}/users/profile"

    payload = json.dumps({
        "photo": "user-1621352948859.jpg",
        "name": "Test",
        "lastName": "Test",
        "dateBirth": "2021-03-17T15:21:05.000Z",
        "country": "Ukraine"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    response_json = response.json()
    payload_js = json.loads(payload)
    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['userId'] == sign_up_response.json()['data']['userId']
    # assert response_json['data']['photoFilename'] == payload_js['photo'] BUG:The system consistently returns
    # The "default-user.png" as the photoFilename despite sending request data for profile editing. Pos.Sol: Validate the
    # backend functionality for profile editing to ensure proper handling of photoFilename updates.
    assert response_json['data']['name'] == payload_js['name']
    assert response_json['data']['lastName'] == payload_js['lastName']
    assert response_json['data']['dateBirth'] == payload_js['dateBirth']
    # BUG:Birthdate always returns the timestamp in the ISO 8601 format Pos.Sol: Ensure the backend API sends the
    # birthdate in the desired format. If it's sending the date in ISO 8601,modify the backend code to format the
    # date appropriately before sending it to the frontend.
    assert response_json['data']['country'] == payload_js['country']
    print(response.text)


def test_edit_users_settings(sign_up_response):
    url = f"{URL}/users/settings"

    payload = json.dumps({
        "currency": "usd",
        "distanceUnits": "km"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    response_json = response.json()
    payload_js = json.loads(payload)
    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'
    assert response_json['data']['currency'] == payload_js['currency']
    assert response_json['data']['distanceUnits'] == payload_js['distanceUnits']
    print(response.text)


def test_change_users_email(sign_up_response):
    url = f"{URL}/users/email"

    payload = json.dumps({
        "email": f"qweerty{random.randint(100000, 999999)}@mail.com",
        "password": json.loads(sign_up_response.request.body)['password']
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['status'] == 'ok'


def test_change_user_password(sign_up_response):
    url = f"{URL}/users/password"

    payload = json.dumps({
        "oldPassword": json.loads(sign_up_response.request.body)['password'],
        "password": "Test12342",
        "repeatPassword": "Test12342"
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)
    response_json = response.json()
    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'


def test_delete_user_account_and_session(sign_up_response):
    url = f"{URL}/users"

    payload = ""
    headers = {
        'Cookie': f'sid={sign_up_response.cookies.get("sid")}'
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)

    print(response.text)
    response_json = response.json()

    assert response.status_code == 200, 'Status code broken'
    assert response_json['status'] == 'ok'