import os
import requests
import json
import streamlit as st
import pandas as pd


def push_message(title, body):
    # https://gist.github.com/mixsoda/4d7eebdf767432f95f4b66ac19f7e310
    token = os.environ["PUSHBULLET_TOKEN"]
    url = "https://api.pushbullet.com/v2/pushes"

    headers = {"content-type": "application/json", "Authorization": "Bearer " + token}
    data_send = {"type": "note", "title": title, "body": body}

    requests.post(url, headers=headers, data=json.dumps(data_send))


st.dataframe(pd.read_json("data/meas.jsonl", lines=True))

if st.button("Send Msg"):
    push_message(title="vent", body="test")
