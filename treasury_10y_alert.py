import yfinance as yf
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def get_10y_yield():
    tnx = yf.Ticker("^TNX")
    data = tnx.history(period="1d", interval="5m")
    latest = data["Close"].iloc[-1]
    return round(latest / 10, 3)

def send_email(yield_value):
    msg = EmailMessage()
    msg["Subject"] = "10-Year Treasury Yield (Hourly)"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    msg.set_content(
        f"""10-Year Treasury Yield Update

Time (UTC): {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}
Yield: {yield_value}%

Source: Yahoo Finance (^TNX)
"""
    )

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    send_email(get_10y_yield())
