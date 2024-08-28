import os
import json
try:
    import requests
except ModuleNotFoundError:
    os.system('pip install requests')
    import requests
try:
    from configparser import ConfigParser
except ModuleNotFoundError:
    os.system('pip install configparser')
    from configparser import ConfigParser
from datetime import datetime
try:
    import pytz
except ModuleNotFoundError:
    os.system('pip install pytz')
    import pytz
# Read configuration
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
config_obj = ConfigParser()
config_obj.read(parent_dir + r"\Configurations\api_config.ini")

class APIClient:
    """Class for handling API calls and processing responses."""

    def __init__(self) -> None:
        """
        Initialize the APIClient.

        Args:
            config_obj (ConfigParser): ConfigParser object containing configuration settings.

        """
        self.config_obj = config_obj
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    def get_config(self,component: str, header: str) -> str:
        """
        Get configuration value from the configuration file.

        Args:
            header (str): Header or key in the configuration file.
            component (str): Component or section in the configuration file.

        Returns:
            str: Configuration value for the specified header and component.
        """
        return self.config_obj[component][header]

    def post_details(self, data):
        url = self.get_config('URL', 'post')
        payload = json.loads(self.get_config('PAYLOAD', 'post'))
        headers = json.loads(self.get_config('HEADER', 'post'))
        for key in payload.keys():
            payload[key] = data[key]
        response = requests.request("POST", url, json=payload, headers=headers)
        return response
        # print(type(response.text))

    def process_data(self, data):
        processed_data = {}
        processed_data['name'] = self.get_config('TEAM', 'stepin')
        if 'date_time' in data.keys():
            date_time = data['date_time']
            print(f'{date_time = }')

            # Input date string
            date_str = data['date_time']
            # Remove the time zone part from the date string
            date_str_without_tz = date_str[:-4]

            # Convert the date string to a datetime object
            date_obj = datetime.strptime(date_str_without_tz, "%B %d, %Y %H:%M")

            # Define the time zone
            ist = pytz.timezone('Asia/Kolkata')

            # Localize the datetime object to IST
            date_obj = ist.localize(date_obj)

            # Format the datetime object to DDMMYYYY
            formatted_date = date_obj.strftime("%d%m%Y")

            # Print the formatted date
            print(formatted_date)
            processed_data['price'] = formatted_date


        if 'link' in data.keys():
            processed_data['item_type'] = data['link']

        if 'headline' in data.keys():
            processed_data['description'] = data['headline']

        if 'strProductName' in data.keys():
            processed_data['item_type'] = data['strProductName']

        if 'strProductDesc' in data.keys():
            processed_data['description'] = data['strProductDesc']

        if 'strProductPrice' in data.keys():


            processed_data['price'] = data['strProductPrice'].replace("₹", "").replace("â‚¹","")


        print(f'{processed_data = }')
        return processed_data

    def fetch_details(self):
        url = self.get_config('URL', 'get')
        payload = ""
        headers = json.loads(self.get_config('HEADER', 'get'))
        response = requests.request("GET", url, data=payload, headers=headers)
        return response

    def fetch_details_by_id(self, id):
        url = self.get_config('URL', 'get')
        if url.endswith('/'):
            url = f'{url}{id}'
        else:
            url = f'{url}/{id}'

        payload = ""
        headers = json.loads(self.get_config('HEADER', 'get'))

        response = requests.request("GET", url, data=payload, headers=headers)

        return response




if __name__ == '__main__':


    # Initialize API client
    api_client = APIClient()
    data = {'link': 'https://indianexpress.com/article/business/ai-loan-sanctioning-rbi-governor-das-9534032/',
            'date_time': 'August 27, 2024 09:35 IST',
            "headline": """For ‘frictionless credit’, RBI to launch technology platform; to call it Unified Lending Interface: Governor Shaktikanta Das"""
           }
    data = {'strProductName': 'JBL Wireless Earbuds', 'strProductDesc': 'High-quality wireless earbuds with noise cancellation and 20 hours of battery life.', 'strProductPrice': '₹5999.0', 'strTeamName': 'Epsilon Team 2'}
    data = api_client.process_data(data)
    post_response = api_client.post_details(data)
    id = json.loads(post_response.text)['id']
    print(f'\n\n{post_response = }')
    all_response = api_client.fetch_details()
    print(f'\n\n{all_response = }')
    id_response = api_client.fetch_details_by_id(id)
    print(f'\n\n{id_response.text = }')
    # response = requests.request("POST", url, json=payload, headers=headers)
    # print(json.loads(response.text))
    # print(type(response.text))


