from unms_api.api import unms_api
from config import config


api = unms_api(config['api_url'], config['api_key'])

response = api.do_request('devices')
print(response)
