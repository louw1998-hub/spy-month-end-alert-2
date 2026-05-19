import yfinance as yf
import pandas as pd

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

# Check if this is month-end
is_month_end = (
    latest_market_day.month !=
    (latest_market_day + pd.Timedelta(days=1)).month
)

print(f"SPY Close: {latest_close:.2f}")
print(f"200 SMA: {sma200:.2f}")
print(f"Is Month End: {is_month_end}")

# Trigger GitHub notification by failing workflow
if is_month_end and latest_close < sma200:

    raise Exception(
        f"ALERT: SPY BELOW 200-DAY SMA | "
        f"Close={latest_close:.2f} | "
        f"SMA200={sma200:.2f}"
    )

print("No signal.")
