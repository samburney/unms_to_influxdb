import requests


class unms_api:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

        pass

    def do_request(self, request, method="GET"):
        method = method.upper()

        headers = {
            'x-auth-token': self.api_key,
        }

        response = requests.request(
            method,
            f'{self.api_url}/{request}',
            headers=headers,
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
