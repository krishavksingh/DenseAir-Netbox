import argparse
from netbox import *
import urllib3
import sys
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
OUTPUT_FILE = 'output.json'



def resolve_references(data, headers):
    newdata = []
    for item in data:  # device items

        new_item = item.copy()  # Create a copy to modify
        for key, value in item.items():  # device items properties

            if isinstance(value, dict):

                for key1, value1 in value.items(): 
                    if key1 == 'url':
                        url = value1
                       # print(f'Removing reference at {url}.')
                        new_data = fetch_data(url, headers)
                        if new_data is not None:
                            new_item[key] = new_data  # Assign fetched data

                    elif isinstance(value1, dict):    # Device properties' properties
                        for key2, value2 in value1.items():
                            if key2 == 'url':
                                url = value2
                        #        print(f'Removing reference at {url}.')
                                new_data1 = fetch_data(url, headers)
                                if new_data1 is not None:
                                    new_item[key][key1] = new_data1  # Assign fetched data

        newdata.append(new_item)  # Add the modified item to the new list

    return newdata

parser = argparse.ArgumentParser(description='Filter Netbox results')

parser.add_argument('--filter', type=str, help='Filter the fetched data from the netbox APIs')
parser.add_argument('--token', type=str, help='Input your API token for the relevant API')
parser.add_argument('--api', type=str, help='Input the api URL that you wish to search from', nargs=None)

args = parser.parse_args()

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token ' + args.token
}

url = build_url(args.api, args.filter)

print('Contacting Netbox at', url, file=sys.stdout)

try:
    data = fetch_data(url, headers)

except Exception as e:
    print('Invalid URL or request failed:', e, file=sys.stderr)
    sys.exit(1)

if not data:
    print('No data received', file=sys.stderr)
    sys.exit(1)

data = data['results'] # Remove unnecessary data from response
data = resolve_references(data, headers)

print('Received:', len(data), 'objects', file=sys.stdout)

with open(OUTPUT_FILE, "w") as output:
    results = json.dumps(data, indent=4)
    output.write(results)

sys.exit(0)
