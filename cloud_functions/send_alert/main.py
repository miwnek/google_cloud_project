import json
import smtplib
import base64
import os
from email.message import EmailMessage
from google.cloud import secretmanager

def main(event, context):
    raw = event["data"]
    decoded = base64.b64decode(raw).decode('utf-8')
    try:
        message = json.loads(decoded)
    except json.JSONDecodeError:
        message = decoded

    if message["status"] != 200:
        send_email_alert(message)

def send_email_alert(data):
    client = secretmanager.SecretManagerServiceClient()
    name = lambda x: f"projects/original-mason-480715-v1/secrets/{x}/versions/latest"
    smtp_user = client.access_secret_version(name=name("SMTP_USER")).payload.data.decode("UTF-8")
    smtp_pass = client.access_secret_version(name=name("SMTP_PASS")).payload.data.decode("UTF-8")
    smtp_target = client.access_secret_version(name=name("SMTP_USER")).payload.data.decode("UTF-8")

    msg = EmailMessage()
    msg["Subject"] = "[GCP] URL unavailable"
    msg["From"] = smtp_user
    msg["To"] = smtp_target
    msg.set_content(
        f"""
        -----------------------------------
        URL {data["url"]} jest niedostępny.
        Status: {data["status"]}"
        -----------------------------------
        """
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

    print("Email sent.")