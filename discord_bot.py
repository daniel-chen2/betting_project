import json
import requests

webhook_url = "https://discord.com/api/webhooks/1401048584912244796/94YuNQ44rXP3dMK15ccwLQ-nsZE3oqwelDxtFJHJlyyPZeofkSWiAP6t-xc1Z2uiSYN2"  # Replace with your actual webhook URL

def send_message(message:str, csv_file_path):
    message_content = {"content": message}

    # Prepare the payload for the webhook
    with open(csv_file_path, "rb") as f:
        files = {
            "file": (csv_file_path, f, "text/csv"),  # (filename, file_object, content_type)
            "payload_json": (None, json.dumps(message_content), "application/json")
        }
        
        response = requests.post(webhook_url, files=files)

        if response.status_code == 204:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
        