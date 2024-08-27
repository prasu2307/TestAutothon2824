import pytest
import requests

@pytest.mark.requestsapidata
# GET method to retrieve data
def test_get_data():
    response = requests.get('https://fake-json-api.mock.beeceptor.com/users')
    data=response.json()
    status_code = response.status_code
    assert status_code == 200
    print(data)
    first_names = [entry['name'].split()[0] for entry in data]
    # print('first name is ',first_names)
    print('first name is ',data[0]['name'])
    # return jsonify({"data": data_store}), 200

@pytest.mark.requestsapidata
# Post Method to post the data
def test_make_post_request():
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
