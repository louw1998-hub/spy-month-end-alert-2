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

# Get close prices
close = spy["Close"].dropna()

# Latest values
latest_close = close.iloc[-1].item()
sma200 = close.tail(200).mean().item()

# Latest trading day
latest_market_day = close.index[-1]

# Detect final trading day of month
is_month_end = (
    latest_market_day.month !=
    (latest_market_day + pd.Timedelta(days=1)).month
)

print(f"SPY Close: {latest_close:.2f}")
print(f"200 SMA: {sma200:.2f}")
print(f"Is Month End: {is_month_end}")

# Trigger alert by failing workflow
if is_month_end and latest_close < sma200:

    raise Exception(
        f"ALERT: SPY BELOW 200-DAY SMA | "
        f"Close={latest_close:.2f} | "
        f"SMA200={sma200:.2f}"
    )

print("No signal.")
