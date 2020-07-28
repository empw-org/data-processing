# EMPW - Data Science

## First Step

- The admin creates a new sensor.
- The user links the created sensor to his account.
- The sesnor sends consumption data.

```json
{
  "sensor_id": "5f1efd8e2514f800017a1fd4",
  "water_level": 126
}
```

## Second Step

A script is scheduled to run every day and gets the consumption data for every registered sensor from the API.

```json
[
  {
    "sensor_id": "5f1efd8e2514f800017a1fd4",
    "date": "2020-07-28T00:00:00.000Z",
    "data": [
      {
        "water_level": 126.0,
        "created_at": "2020-07-28T04:15:19.554Z"
      },
      {
        "water_level": 128.0,
        "created_at": "2020-07-28T04:30:22.698Z"
      },
      {
        "water_level": 230.0,
        "created_at": "2020-07-28T05:38:03.936Z"
      }
    ]
  },
  {
    "sensor_id": "5f1efd542514f800017a1fcc",
    "date": "2020-07-28T00:00:00.000Z",
    "data": [
      {
        "water_level": 100.0,
        "created_at": "2020-07-28T05:15:00.391Z"
      },
      {
        "water_level": 123.0,
        "created_at": "2020-07-28T05:30:02.945Z"
      },
      {
        "water_level": 13.0,
        "created_at": "2020-07-28T06:26:43.864Z"
      },
      {
        "water_level": 20.0,
        "created_at": "2020-07-28T06:50:53.828Z"
      }
    ]
  }
]
```

The script processes the data and returns back to the API the consumption statistics.

```json
[
  {
    "sensor_id": "5f1efd8e2514f800017a1fd4",
    "date": "2020-07-28",
    "consumption": 104
  },
  {
    "sensor_id": "5f1efd542514f800017a1fcc",
    "date": "2020-07-28",
    "consumption": 30
  }
]
```

This data is stored and provided to the users.

## Third step

In the frontend(web/mobile), the users sees charts and statistics for his/her water consumption.
