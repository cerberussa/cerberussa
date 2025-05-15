import smtplib
from email.message import EmailMessage
import requests
import os

# === EMAIL ALERT ===
def send_email_alert(subject, body, to_email="contact@bcrealestate.ch"):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("ALERT_EMAIL_FROM", "alerts@dingdong.ai")
    msg["To"] = to_email

    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)

# === TELEGRAM ALERT ===
def send_telegram_alert(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("ALERT_CHAT_ID", "@Cerberussa")  # or user ID
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    requests.post(url, data=payload)

# === EXAMPLE USAGE ===
def alert_manager(service, client, time, urgent=False):
    text = f"New Booking Alert:\nService: {service}\nClient: {client}\nTime: {time}"
    if urgent:
        text += "\n‼️ URGENT BOOKING ‼️"

    send_email_alert(f"[DingDong] New Booking – {service}", text)
    send_telegram_alert(text)
