import pandas as pd
from datetime import date
import requests
import os

BASE_URL = os.environ['EMPW_API_BASE_URL']
ADMIN_EMAIL = os.environ['ADMIN_EMAIL']
ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']


def get_day(row):
    return row["created_at"].weekday()


def absolute_value(row):
    return max(row['water_level'], 0)


def remove_time(row):
    return pd.Timestamp(date(row["created_at"].year, row["created_at"].month, row["created_at"].day))


def query_by_date(data, fromYear, fromMonth, fromDay, toYear, toMonth, toDay):
    return data[(data["date"] > pd.Timestamp(date(fromYear, fromMonth, fromDay)))
                & (data["date"] < pd.Timestamp(date(toYear, toMonth, toDay)))]


def get_admin_token():
    url = '{}/admins/login'.format(BASE_URL)
    response = requests.post(
        url, data={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    json = response.json()
    if response.ok:
        return json['token']
    else:
        print(json)
        raise Exception(
            '[Get Admin Token] Got {}'.format(response.status_code))


def get_data():
    token = get_admin_token()
    url = '{}/consumption_reports'.format(BASE_URL)
    response = requests.get(
        url, headers={'authorization': 'bearer {}'.format(token)})

    json = response.json()
    if response.ok:
        return json
    else:
        print(json)
        raise Exception('[Get Data] Got {}'.format(response.status_code))


if __name__ == "__main__":

    data = pd.read_excel("input.xlsx")
    data = data.set_index('entry_id')

    data['water_level'] = data['field1'] - data['x']
    data['water_level'] = data.apply(absolute_value, axis=1)

    data = data[data['water_level'] != 0]

    data["days"] = data.apply(get_day, axis=1)
    data["date"] = data.apply(remove_time, axis=1)

    data = query_by_date(data, 2018, 2, 20, 2018, 3, 12)

    groubedData = data.groupby("date").sum()

    dataToDrow = pd.DataFrame({"usage": groubedData["water_level"]})
    dataToDrow.to_csv("output.csv")
