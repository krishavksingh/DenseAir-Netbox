import requests
import sys


def build_url(api, filter_string): 
    '''
    Creates a valid url if api and filter string are both valid
    '''
    return api + '?manufacturer=' + filter_string.lower()


def fetch_data(url, headers): 
    '''
    Fetches data from netbox apis
    '''
    payload = {}

    response = requests.request('GET', url,
                                headers=headers,
                                data=payload,
                                verify=False)

    if str(response) == '<Response [403]>':
        print('Access forbidden - invalid API key', file=sys.stderr)
        sys.exit(1)

    return response.json()

