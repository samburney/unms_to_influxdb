import influxdb
import datetime

from unms_api.api import unms_api
from config import config


api = unms_api(config['api_url'], config['api_key'])

influx_interfaces = []
response = api.do_request('devices')
if response is not None:
    devices = response
    for device in devices:
        response = api.do_request(f"devices/{device['identification']['id']}/interfaces")
        if response is not None:
            interfaces = response

            for interface in interfaces:
                if device['identification']['site'] is not None and device['identification']['model'] != 'UNKNOWN':
                    influx_interface = {
                        "measurement": "interface",
                        "tags": {
                            "site_name": device['identification']['site']['name'],
                            "device_name": device['identification']['name'],
                            "device_hostname": device['identification']['hostname'],
                            "device_status": device['overview']['status'],
                            "device_type": device['identification']['type'],
                            "device_model": device['identification']['model'],
                            "interface_type": interface['identification']['type'],
                            "interface_name": interface['identification']['name'],
                            "interface_description": interface['identification']['description'],
                        },
                        "fields": interface['statistics'],
                        "time": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                    }
                    influx_interfaces.append(influx_interface)

if len(influx_interfaces) > 0:
    influx_client = influxdb.InfluxDBClient(
        host=config['influxdb_host'],
        username=config['influxdb_user'],
        password=config['influxdb_pass'],
        database=config['influxdb_db'],
    )
    influx_client.write_points(influx_interfaces)
