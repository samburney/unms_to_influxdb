import argparse
import ipaddress

from unms_api.api import unms_api
from config import config


def parse_arguments():
    parser = argparse.ArgumentParser(description='Collect UNMS devices and build list of LibreNMS nets to discover from')
    parser.add_argument('-o', '--output', help='Output file', required=True)
    parser.add_argument('-i', '--interface-type', help='Interface type to filter by')
    parser.add_argument('--exclude-private', help='Exclude RF1918 private addresses', action='store_true')

    return parser.parse_args()


def main():
    api = unms_api(config['api_url'], config['api_key'])
    args = parse_arguments()

    response = api.do_request('devices')
    if response is not None:
        devices = response
        for device in devices:
            response = api.do_request(f"devices/{device['identification']['id']}/interfaces")
            if response is not None:
                interfaces = response

                for interface in interfaces:
                    if args.interface_type is not None:
                        if interface['identification']['type'] != args.interface_type:
                            continue

                    if 'addresses' in interface:
                        for address in interface['addresses']:
                            if 'cidr' in address:
                                address_parts = address['cidr'].split('/')

                                # Honour --exclude-private argument
                                if args.exclude_private is True and ipaddress.ip_network(address_parts[0]).is_private:
                                    continue

                                print(address['cidr'])


if __name__ == "__main__":
    main()