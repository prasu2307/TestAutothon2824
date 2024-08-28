import os
import json
try:
    import pytest
except ModuleNotFoundError:
    os.system('pip install pytest')
    import pytest
import requests
import allure
from HelperClasses.API.Base import APIClient
import ast
current_dir = os.path.dirname(os.path.realpath(__file__))
print(f'{current_dir = }')
parent_dir = os.path.dirname(current_dir)
api_client = APIClient()

# Post Method to post the data
# Function to compare POST and GET data
def compare_post_get_data(post_data, get_data, counter):
    allure.attach(str(post_data), f"Post Results {counter}")
    allure.attach(str(get_data), f"Get Results {counter}")

    return post_data == get_data


@pytest.mark.validateapi
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_api():
    with open(parent_dir + '/Outputs/ActualOutputs/news_information_ui_result.txt', 'r') as file:
        ui_data_list = file.read()
    with open(parent_dir + '/Outputs/ActualOutputs/product_information_apk_result.txt', 'r') as file:
        apk_data_list = file.read()

    ui_data_list = ast.literal_eval(ui_data_list)
    print(ui_data_list)
    apk_data_list = ast.literal_eval(apk_data_list)
    print(apk_data_list)
    ui_data_list.extend(apk_data_list)
    counter = 0
    # Process each UI data
    for ui_data in ui_data_list:
        counter += 1
        with allure.step(f'Validating API {counter}'):
            data = api_client.process_data(ui_data)
            post_response = api_client.post_details(data)

            print("POST Response Text:", post_response.text)
            print("POST Response Status Code:", post_response.status_code)
            allure.attach(str(post_response.status_code), f'Post Status Code {counter}')
            assert post_response.status_code == 200, f"Invalid Status Code returned: {post_response.status_code}"
            # Extract ID from POST response
            post_data = json.loads(post_response.text)
            id = post_data['id']

            # Fetch data using the ID
            id_response = api_client.fetch_details_by_id(id)
            allure.attach(str(id_response.status_code), f'GET Status Code {counter}')
            assert id_response.status_code == 200, f"Invalid Status Code returned: {id_response.status_code}"
            get_data = json.loads(id_response.text)

            print("GET Response Text:", id_response.text)

            # Compare POST and GET data

            is_data_equal = compare_post_get_data(post_data, get_data, counter)
            print("Is POST data equal to GET data?", is_data_equal)
            assert is_data_equal, "Data is not Equal"

    # for apk_data in apk_data_list:
    #     data = api_client.process_data(apk_data)
    #     post_response = api_client.post_details(data)
    #     id = post_response['id']
    #     id_response = api_client.fetch_details_by_id(id)