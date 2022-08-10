import requests
import settings
import datetime

if __name__ == "__main__":

    now = datetime.datetime.now()

    response = requests.post("{}/events".format(settings.API_ENDPOINT), {
        "start": now.strftime("%Y-%m-%d %H:%M:%S"),
        "duration": 300,
        "description": "Work",
    })
    now.replace(day=now.day + 1)
    requests.post("{}/events".format(settings.API_ENDPOINT), data={
        "start": now.strftime("%Y-%m-%d %H:%M:%S"),
        "duration": 60,
        "description": "Gym",
    })
    now.replace(day=now.day + 1, hour=10)
    requests.post("{}/events".format(settings.API_ENDPOINT), data={
        "start": now.strftime("%Y-%m-%d %H:%M:%S"),
        "duration": 300,
        "description": "Work",
    })
    now.replace(day=now.hour + 3)
    requests.post("{}/events".format(settings.API_ENDPOINT), data={
        "start": now.strftime("%Y-%m-%d %H:%M:%S"),
        "duration": 30,
        "description": "Gym",
    })
    now.replace(day=now.day + 1)
    requests.post("{}/events".format(settings.API_ENDPOINT), data={
        "start": now.strftime("%Y-%m-%d %H:%M:%S"),
        "duration": 60,
        "description": "Gym",
    })
