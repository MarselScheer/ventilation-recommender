import os
import requests
import json
import pandas as pd
from datetime import datetime
import time


class Notification:
    def send(self, title: str, body: str):
        # https://gist.github.com/mixsoda/4d7eebdf767432f95f4b66ac19f7e310
        token = os.environ["PUSHBULLET_TOKEN"]
        url = "https://api.pushbullet.com/v2/pushes"

        headers = {
            "content-type": "application/json",
            "Authorization": "Bearer " + token,
        }
        data_send = {"type": "note", "title": title, "body": body}

        requests.post(url, headers=headers, data=json.dumps(data_send))


class NotificationDummy:
    def send(self, title: str, body: str):
        print(title, body)


class Sensor:
    def get_measurements(self) -> dict:
        pass


class SensorDummy:
    def get_measurements(self) -> dict:
        from random import randrange

        return dict(
            timestamp=datetime.now(),
            temperature=randrange(10, 30),
            humidity=randrange(70, 85),
        )


class Alert:
    def __init__(self, sender: Notification) -> None:
        self.threshold = 70
        self.min_elapsed_time = 3
        self.sender = sender
        self.sender.send(title="Alert system up", body=f"Threshold = {self.threshold}")
        self.last_alert = datetime.now()

    def check(self, value: float) -> None:
        hour = int(datetime.now().strftime("%H"))
        if hour < 8 or 22 < hour:
            return
        elapsed_time = (datetime.now() - self.last_alert).total_seconds()
        if self.threshold < value and self.min_elapsed_time < elapsed_time:
            self.sender.send(title="Humidity too high", body=str(value))
            self.last_alert = datetime.now()


sender = NotificationDummy() if os.environ["DEVELOPMENT"] else Notification()
alert_system = Alert(sender=sender)
sensor = SensorDummy() if os.environ["DEVELOPMENT"] else Sensor()
WAIT = 1 if os.environ["DEVELOPMENT"] else 60
measurements = []
while True:
    pd.DataFrame(measurements).to_json("data/meas.jsonl", lines=True, orient="records")
    meas = sensor.get_measurements()
    measurements.append(meas)
    alert_system.check(value=meas["humidity"])

    time.sleep(WAIT)
