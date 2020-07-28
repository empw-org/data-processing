import os

import requests
from dotenv import load_dotenv

load_dotenv()


def get_admin_token():
    print('[get_admin_token] Started')
    url = '{}/admins/login'.format(API_BASE_URL)
    response = requests.post(
        url, json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    json = response.json()
    if response.ok:
        return json['token']
    else:
        print(json)
        raise Exception(
            '[get_admin_token] Got {}'.format(response.status_code))


def get_consumption_data():
    print('[get_consumption_data] Started')
    url = '{}/consumption_data'.format(API_BASE_URL)
    response = requests.get(
        url, headers={'authorization': 'bearer {}'.format(TOKEN)})

    json = response.json()
    if response.ok:
        return json
    else:
        print(json)
        raise Exception(
            '[get_consumption_data] Failed! Got {}'.format(response.status_code))


def send_consumption_reports(reports):
    print('[send_consumption_reports] Started')

    url = '{}/consumption_reports'.format(API_BASE_URL)

    response = requests.post(
        url,
        json={'reports':  reports},
        headers={'authorization': 'bearer {}'.format(TOKEN)})

    if response.ok:
        print('[send_consumption_reports] Data has been sent to the API successfully')
    else:
        raise Exception(
            '[send_consumption_reports] Failed! Got {}'.format(response.status_code))


API_BASE_URL = os.environ['API_BASE_URL']
ADMIN_EMAIL = os.environ['ADMIN_EMAIL']
ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']
TOKEN = get_admin_token()
