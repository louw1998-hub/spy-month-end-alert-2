import yfinance as yf
import pandas as pd
import smtplib
from email.message import EmailMessage
import os

# Download SPY daily data
spy = yf.download(
    "SPY",
    period="260d",
    interval="1d",
    auto_adjust=True,
    progress=False
)

# Closing prices
close = spy["Close"].dropna()

latest_close = float(close.iloc[-1])
sma200 = float(close.tail(200).mean())

# Latest trading day
latest_market_day = close.index[-1]

# Determine if this is the final trading day of the month
is_month_end = (
    latest_market_day.month !=
    (latest_market_day + pd.Timedelta(days=1)).month
)

print(f"SPY Close: {latest_close:.2f}")
print(f"200 SMA: {sma200:.2f}")
print(f"Is Month End: {is_month_end}")

if is_month_end and latest_close < sma200:

    print("Signal triggered. Sending email...")

    msg = EmailMessage()

    msg["Subject"] = "SPY BELOW 200-DAY SMA (MONTH END)"
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = os.environ["EMAIL_TO"]

    msg.set_content(
        f"SPY closed below its 200-day SMA "
        f"on the final trading day of the month.\n\n"
        f"SPY Close: {latest_close:.2f}\n"
        f"200-Day SMA: {sma200:.2f}"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            os.environ["EMAIL_USER"],
            os.environ["EMAIL_PASS"]
        )
        smtp.send_message(msg)

    print("Email sent.")

else:
    print("No signal.")
