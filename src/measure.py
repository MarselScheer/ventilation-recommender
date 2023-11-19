import os
import requests
import json

# import pandas as pd
from datetime import datetime
import time


def is_development():
    return os.getenv("DEVELOPMENT") is not None


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
    def __init__(self) -> None:
        import Adafruit_DHT

        self.sensor = Adafruit_DHT.DHT22
        self.pin = 4

    def get_measurements(self) -> dict:
        import Adafruit_DHT

        meas_avail = False
        while not meas_avail:
            time.sleep(1)
            hum, temp = Adafruit_DHT.read(self.sensor, self.pin)
            meas_avail = hum is not None and temp is not None

        return dict(
            timestamp=f"{datetime.now()}",
            temperature=temp,
            humidity=hum,
        )

        pass


class SensorDummy:
    def get_measurements(self) -> dict:
        from random import randrange

        return dict(
            timestamp=f"{datetime.now()}",
            temperature=randrange(10, 30),
            humidity=randrange(70, 85),
        )


class Alert:
    def __init__(self, sender: Notification) -> None:
        self.threshold = 70
        self.min_elapsed_time = 1 if is_development() else 30 * 60
        self.sender = sender
        self.sender.send(
            title="Alert system up",
            body=f"Threshold = {self.threshold}\n{datetime.now()}",
        )
        self.last_alert = datetime.now()

    def check(self, value: float) -> None:
        hour = int(datetime.now().strftime("%H"))
        if hour < 8 or 22 < hour:
            return
        elapsed_time = (datetime.now() - self.last_alert).total_seconds()
        if self.threshold < value and self.min_elapsed_time < elapsed_time:
            self.sender.send(
                title="Humidity too high", body=f"{value}\n{datetime.now()}"
            )
            self.last_alert = datetime.now()


sender = NotificationDummy() if is_development() else Notification()
alert_system = Alert(sender=sender)
sensor = SensorDummy() if is_development() else Sensor()
WAIT = 1 if is_development() else 60
measurements = []


def write_meas(m):
    with open("data/meas.jsonl", "a") as fh:
        json.dump(m, fh)
        fh.write("\n")


while True:
    # pd.DataFrame(measurements).to_json("data/meas.jsonl", lines=True, orient="records")
    meas = sensor.get_measurements()
    measurements.append(meas)
    write_meas(m=meas)
    alert_system.check(value=meas["humidity"])

    time.sleep(WAIT)
