from datetime import datetime
from timeit import default_timer as timer

import pandas as pd

import api


def to_date(row):
    return datetime.strptime(row['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').date()


def non_negatives_only(row):
    return max(row['water_level'], 0)


def calculate_consumption(data):
    data = pd.DataFrame(pd.DataFrame.from_dict(data))
    water_level = data['water_level'].tolist()
    water_level.insert(0, water_level[0])
    water_level.pop()
    data['water_level'] = data["water_level"] - water_level
    data['water_level'] = data.apply(non_negatives_only, axis=1)
    return data['water_level'].sum()


if __name__ == "__main__":
    consumption_data = api.get_consumption_data()
    consumption_reports = []
    print('[processing data] Started')
    print('[processing data] Processing data from {} sensors'
          .format(len(consumption_data)))
    start = timer()

    for sensor_data in consumption_data:
        consumption_reports.append({
            "sensor_id": sensor_data['sensor_id'],
            "date": sensor_data['date'],
            'consumption': calculate_consumption(sensor_data['data']),
        })

    end = timer()
    print('[processing data] Done')
    print('[processing data] Took: {} Seconds'.format(end - start))
    api.send_consumption_reports(consumption_reports)
