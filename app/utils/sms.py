import os
from twilio.rest import Client
from app import dotenv_path
from dotenv import load_dotenv

load_dotenv(dotenv_path)

# setup twilio auth
account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)


def send_sms(body, sender, receiver):
    message = client.messages \
        .create(
            body=body,
            from_=sender,
            to=receiver
    )
    return message
