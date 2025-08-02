import requests

webhook_url = "https://discord.com/api/webhooks/1401048584912244796/94YuNQ44rXP3dMK15ccwLQ-nsZE3oqwelDxtFJHJlyyPZeofkSWiAP6t-xc1Z2uiSYN2"  # Replace with your actual webhook URL
message_content = {"content": "Hello from Python!"}

def send_message(message:str):
    response = requests.post(webhook_url, json={"content": message})

    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")