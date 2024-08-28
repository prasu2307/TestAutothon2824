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
try:
    from tabulate import tabulate
except ModuleNotFoundError:
    os.system('pip install tabulate')
    from tabulate import tabulate
current_dir = os.path.dirname(os.path.realpath(__file__))
print(f'{current_dir = }')
parent_dir = os.path.dirname(current_dir)
api_client = APIClient()


# Post Method to post the data
# Function to compare POST and GET data
def compare_post_get_data(expected_data, actual_data, counter):
    expected_data = {key: expected_data[key] for key in sorted(expected_data)}
    actual_data = {key: actual_data[key] for key in sorted(actual_data)}
    print(f'{expected_data = }')
    print(f'{actual_data = }')
    allure.attach(str(expected_data), f"Expected Response {counter}")
    allure.attach(str(actual_data), f"Actual Response {counter}")
    return expected_data == actual_data


def compare_data_types(expected_data, actual_data, counter):
    expected_data = {key: expected_data[key] for key in sorted(expected_data)}
    actual_data = {key: actual_data[key] for key in sorted(actual_data)}

    expected_types = [(key, type(expected_data[key])) for key in expected_data]
    actual_types = [(key, type(actual_data[key])) for key in actual_data]

    # Create tables
    expected_table = tabulate(expected_types, headers=["Key", "Expected Type"], tablefmt="grid")
    actual_table = tabulate(actual_types, headers=["Key", "Actual Type"], tablefmt="grid")
    print(f'\n{expected_table}')
    print(f'\n{actual_table}')
    # Attach tables to the Allure report
    allure.attach(expected_table, name="Expected Data Types", attachment_type=allure.attachment_type.TEXT)
    allure.attach(actual_table, name="Actual Data Types", attachment_type=allure.attachment_type.TEXT)

    mismatches = []

    for key in expected_data:
        expected_type = type(expected_data[key])
        actual_type = type(actual_data[key])

        if expected_type != actual_type:
            mismatches.append((key, expected_type, actual_type))

    if mismatches:
        for key, expected_type, actual_type in mismatches:
            allure.attach(f"Datatype Mismatch in API {counter} for {key}: expected {expected_type}, got {actual_type}",
                          name=f"Datatype Mismatch in API {counter} for {key}", attachment_type=allure.attachment_type.TEXT)
            print(f"Datatype Mismatch in API {counter} for {key}: expected {expected_type}, got {actual_type}")
        return False

    return True


def validate_api(ui_data_list):
    counter = 0
    failed_count = 0
    failures = []
    # Process each UI data
    for ui_data in ui_data_list:
        counter += 1
        print(f'{ui_data = }')
        with allure.step(f'Validating API {counter}'):
            data = api_client.process_data(ui_data)
            try:
                post_response = api_client.post_details(data)
            except requests.exceptions.ConnectionError as e:
                failed_count += 1
                failures.append(str(e))
                allure.attach(str(e), "HTTP Connection Error for POST API")
                continue

            print("POST Response Text:", post_response.text)
            print("POST Response Status Code:", post_response.status_code)
            allure.attach(str(post_response.status_code), f'Post Status Code {counter}')
            try:
                assert post_response.status_code == 200, f"Invalid Status Code for API {counter}: Returned status code: {post_response.status_code}"
            except AssertionError as e:
                failed_count += 1
                failures.append(str(e))

                continue
            
            # Extract ID from POST response
            post_data = json.loads(post_response.text)
            id = post_data['id']
            allure.attach(str(post_data), f"Post Response {counter}")
            del post_data['id']
            is_data_equal = compare_post_get_data(data, post_data, counter)
            try:
                assert is_data_equal, f"Post Response for API {counter}: Data is not as expected"
            except AssertionError as e:
                failed_count += 1
                failures.append(str(e))

            is_data_type_equal = compare_data_types(data, post_data, counter)
            try:
                assert is_data_type_equal, f"Post Response for API {counter}: Datatype(s) is/are not as expected"
            except AssertionError as e:
                failed_count += 1
                failures.append(str(e))

            # Fetch data using the ID
            try:
                id_response = api_client.fetch_details_by_id(id)
            except requests.exceptions.ConnectionError as e:
                failed_count += 1
                failures.append(str(e))
                allure.attach(str(e), "HTTP Connection Error for GET API")
                continue

            allure.attach(str(id_response.status_code), f'GET Status Code {counter}')
            try:
                assert id_response.status_code == 200, f"Invalid Status Code for API {counter}: Returned status code: {id_response.status_code}"
            except AssertionError as e:
                failed_count += 1
                failures.append(str(e))
                continue
            get_data = json.loads(id_response.text)

            print("GET Response Text:", id_response.text)

            # Compare POST and GET data
            del get_data['id']
            is_data_equal = compare_post_get_data(data, get_data, counter)
            print("Is POST data equal to GET data?", is_data_equal)
            try:
                assert is_data_equal, f"GET Response for API {counter}: Data is not as expected"
            except AssertionError as e:
                failed_count += 1
                failures.append(str(e))

            is_data_type_equal = compare_data_types(data, get_data, counter)
            try:
                assert is_data_type_equal, f"GET Response for API {counter}: Datatype(s) is/are not as expected"
            except AssertionError as e:
                failed_count += 1
                failures.append(str(e))

    # if failed_count > 0:
    #     print(f'{failed_count = }')
    #     with allure.step('API Validation Error Information'):
    #         failures = '\n'.join(failures)
    #         failures = failures.replace('\nassert False\n', '\n')
    #         print(f'{failures = }')
    #         assert failed_count == 0, f"Found {failed_count} failure in API Validation\n{failures}"
