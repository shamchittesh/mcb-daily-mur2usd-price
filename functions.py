import os
import requests
import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def download_forex_data(startdate, enddate, currency="USD", basecurrency="MUR", filename="forex_data.xlsx"):
    """Download forex data from MCB website as Excel file."""
    url = "https://mcb.mu/webapi/mcb/ForexDataExcel"

    # Format dates as dd-MMM-yyyy (e.g., 07-Aug-2024)
    if isinstance(startdate, str):
        startdate_str = startdate
    else:
        startdate_str = startdate.strftime('%d-%b-%Y')

    if isinstance(enddate, str):
        enddate_str = enddate
    else:
        enddate_str = enddate.strftime('%d-%b-%Y')

    payload = {
        "StartDate": startdate_str,
        "EndDate": enddate_str,
        "CurrencyCode": currency,
        "BaseCurrency": basecurrency
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"File downloaded successfully and saved as {filename}.")
            return True
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def find_column(df):
    """Find the column containing 'SELLING' and 'TT' headers."""
    column_with_selling_tt = None
    for col in df.columns:
        if "SELLING" in df[col].values and "TT" in df[col].values:
            column_with_selling_tt = col
            break
    return column_with_selling_tt


def get_selling_tt_rates(df, column_with_selling_tt):
    """Extract numeric selling TT rates from the dataframe."""
    if column_with_selling_tt is None:
        print("No rates column found.")
        return pd.Series(dtype=float)

    numeric_values = pd.to_numeric(df[column_with_selling_tt], errors='coerce')
    cleaned = numeric_values.dropna()
    return cleaned


def get_lastprice(df, column_with_selling_tt):
    """Get the most recent selling TT rate."""
    rates = get_selling_tt_rates(df, column_with_selling_tt)
    if rates.empty:
        return None
    last_price = rates.iloc[-1]
    print(f"Last Price (Selling TT): {last_price}")
    return last_price


def get_mean(df, column_with_selling_tt):
    """Calculate the mean of selling TT rates."""
    rates = get_selling_tt_rates(df, column_with_selling_tt)
    if rates.empty:
        return None
    mean_value = rates.mean()
    print(f"Mean (Selling TT): {mean_value:.4f}")
    return mean_value


def get_std(df, column_with_selling_tt):
    """Calculate the standard deviation of selling TT rates."""
    rates = get_selling_tt_rates(df, column_with_selling_tt)
    if rates.empty:
        return None
    std_value = rates.std()
    print(f"Standard Deviation (Selling TT): {std_value:.4f}")
    return std_value


def check_deviation(last_price, mean, std, threshold=2.0):
    """
    Check if the last price deviates from the mean by more than threshold * SD.
    Returns a tuple: (is_deviated: bool, z_score: float, direction: str)
    """
    if std == 0:
        return False, 0.0, "stable"

    z_score = (last_price - mean) / std
    is_deviated = abs(z_score) > threshold

    if z_score > 0:
        direction = "above"
    elif z_score < 0:
        direction = "below"
    else:
        direction = "at"

    print(f"Z-Score: {z_score:.4f} | Threshold: ±{threshold} | Deviated: {is_deviated} ({direction} mean)")
    return is_deviated, z_score, direction


def send_telegram_message(message):
    """Send a message via Telegram Bot API."""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or bot_token == "your_bot_token_here":
        print("ERROR: TELEGRAM_BOT_TOKEN not configured in .env")
        return False
    if not chat_id or chat_id == "your_chat_id_here":
        print("ERROR: TELEGRAM_CHAT_ID not configured in .env")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram message sent successfully!")
            return True
        else:
            print(f"Failed to send Telegram message. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False


def get_market_rate():
    """Fetch the current mid-market USD/MUR rate from a free API."""
    url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rate = data.get("usd", {}).get("mur")
            if rate:
                print(f"Market Rate (USD/MUR): {rate:.4f}")
                return float(rate)
        print(f"Failed to fetch market rate. Status: {response.status_code}")
        return None
    except Exception as e:
        print(f"Error fetching market rate: {e}")
        return None


def calculate_spread(mcb_selling_tt, market_rate):
    """
    Calculate the bank spread percentage.
    Spread = (MCB Selling TT - Market Rate) / Market Rate * 100
    """
    if market_rate is None or market_rate == 0:
        return None
    spread_pct = (mcb_selling_tt - market_rate) / market_rate * 100
    print(f"Spread: {spread_pct:.4f}% (MCB: {mcb_selling_tt:.2f} vs Market: {market_rate:.4f})")
    return spread_pct


def send_spread_alert(mcb_rate, market_rate, spread_pct):
    """Send a Telegram alert when spread is below threshold."""
    message = (
        f"💰 *Low Spread Alert - USD/MUR*\n\n"
        f"*MCB Selling TT:* {mcb_rate:.2f} MUR\n"
        f"*Market Rate:* {market_rate:.4f} MUR\n"
        f"*Bank Spread:* {spread_pct:.2f}%\n\n"
        f"Spread is below 1% — good time to buy USD!"
    )
    return send_telegram_message(message)


def send_test_notification():
    """Send a test notification to verify Telegram setup."""
    message = (
        "🧪 *Test Notification*\n\n"
        "MCB USD/MUR Forex Monitor is working!\n"
        "You will receive alerts when:\n"
        "• Rate deviates significantly from 30-day average\n"
        "• Bank spread drops below 1%"
    )
    return send_telegram_message(message)


def send_alert(last_price, mean, std, z_score, direction, threshold):
    """Send a forex alert notification via Telegram."""
    emoji = "📈" if direction == "above" else "📉"
    message = (
        f"{emoji} *USD/MUR Rate Alert*\n\n"
        f"*Current Rate:* {last_price:.2f} MUR\n"
        f"*30-Day Mean:* {mean:.4f} MUR\n"
        f"*Std Deviation:* {std:.4f}\n"
        f"*Z-Score:* {z_score:.2f} ({direction} mean)\n"
        f"*Threshold:* ±{threshold} SD\n\n"
        f"The rate has moved *{abs(z_score):.2f} standard deviations* {direction} the 30-day average."
    )
    return send_telegram_message(message)
