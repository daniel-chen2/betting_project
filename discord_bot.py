import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

webhook_url = "https://discord.com/api/webhooks/1401048584912244796/94YuNQ44rXP3dMK15ccwLQ-nsZE3oqwelDxtFJHJlyyPZeofkSWiAP6t-xc1Z2uiSYN2"  # Replace with your actual webhook URL

def send_message(message:str, csv_file_path):
    message_content = {"content": message}

    # define the retry strategy
    retry_strategy = Retry(
        total=4,  # maximum number of retries
        backoff_factor=2,
        status_forcelist=[
            429,
            500,
            502,
            503,
            504,
        ],  # the HTTP status codes to retry on
    )

    # create an HTTP adapter with the retry strategy and mount it to the session
    adapter = HTTPAdapter(max_retries=retry_strategy)

    # create a new session object
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Prepare the payload for the webhook
    with open(csv_file_path, "rb") as f:
        files = {
            "file": (csv_file_path, f, "text/csv"),  # (filename, file_object, content_type)
            "payload_json": (None, json.dumps(message_content), "application/json")
        }
        
        response = requests.post(webhook_url, files=files)

        if response.status_code == 204 or response.status_code == 200:
            print("Message sent successfully!")
            print(response.text)
        else:
            print(f"Failed to send message. Status code: {response.status_code}")