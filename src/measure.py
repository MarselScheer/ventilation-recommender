import os
import requests
import json

# import pandas as pd
from datetime import datetime
import time

import logging

logger = logging.getLogger("monitor")
# log to monitor.log and stdout
logging.basicConfig(filename="/tmp/monitor.log", level=logging.INFO)


def is_development():
    """
    Returns true if the app is running in development mode
    """
    return os.getenv("DEVELOPMENT") is not None


class Notification:
    """
    Class for sending notifications
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        logger.info("Init Notification")

    def send(self, title: str, body: str):
        """
        Send a notification
        :param title: Title of the notification
        :param body: Body of the notification
        """
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
    """
    During development, we want to send notifications to stdout
    """

    def __init__(self) -> None:
        logger.info("Init NotificationDummy")

    def send(self, title: str, body: str):
        print(title, body)


class Sensor:
    """
    Class for reading the temperature and humidity
    """

    def __init__(self) -> None:
        """
        Constructor initializing the Sensor
        """
        logger.info("Init Sensor")
        import Adafruit_DHT

        self.sensor = Adafruit_DHT.DHT22
        self.pin = 4

    def get_measurements(self) -> dict:
        """
        Measure the temperature and humidity. Since the sensor can be unreliable
        we loop until we get a measurement sleeping each time for 1 second.
        """
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
    """
    During development the real sensor is not available and we want to simulate
    measurements.
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        logger.info("Init SensorDummy")

    def get_measurements(self) -> dict:
        """
        Make up measurements
        """
        from random import randrange

        return dict(
            timestamp=f"{datetime.now()}",
            temperature=randrange(10, 30),
            humidity=randrange(70, 85),
        )


class Alert:
    """
    Class that monitors humidity and sends a notification if humidity is too high.
    In order to not get spammed with notifications we only send one every 30 minutes.
    Also we only send notifications between 8 and 22 o'clock.
    """

    def __init__(self, sender: Notification) -> None:
        """
        Constructor

        :param sender: Notification class used to send notifications
        """
        logger.info("Init Alert")
        self.threshold = 70
        self.min_elapsed_time = 1 if is_development() else 30 * 60
        self.sender = sender
        self.sender.send(
            title="Alert system up",
            body=f"Threshold = {self.threshold}\n{datetime.now()}",
        )
        self.last_alert = datetime.now()
        logger.info(f"{self.threshold=}, {self.min_elapsed_time=}, {self.sender=}")

    def check(self, value: float) -> None:
        """
        Logic to check and decide when to send a notification
        :param value: Humidity measured by the sensor
        """
        hour = int(datetime.now().strftime("%H"))
        if hour < 8 or 22 < hour:
            return
        elapsed_time = (datetime.now() - self.last_alert).total_seconds()
        if self.threshold < value and self.min_elapsed_time < elapsed_time:
            self.sender.send(
                title="Humidity too high", body=f"{value}\n{datetime.now()}"
            )
            self.last_alert = datetime.now()


def write_meas(m):
    """
    export measurements to data/meas.jsonl
    :param m: list of dicts
    """
    with open("data/meas.jsonl", "a") as fh:
        json.dump(m, fh)
        fh.write("\n")


def main():
    """
    Orchestrate logic to send notifications if humidity is too high via pushbullet
    """
    sender = NotificationDummy() if is_development() else Notification()
    alert_system = Alert(sender=sender)
    sensor = SensorDummy() if is_development() else Sensor()
    WAIT = 1 if is_development() else 60
    measurements = []

    while True:
        # pd.DataFrame(measurements).to_json("data/meas.jsonl", lines=True, orient="records")
        meas = sensor.get_measurements()
        measurements.append(meas)
        write_meas(m=meas)
        alert_system.check(value=meas["humidity"])

        time.sleep(WAIT)


if __name__ == "__main__":
    main()
