"""
MCB USD/MUR Daily Forex Rate Monitor
-------------------------------------
1. Downloads daily exchange rates from MCB website
2. Calculates standard deviation of the selling TT rate
3. Alerts via Telegram if the rate deviates beyond the configured SD threshold
"""

from modules import *


def main():
    # --- Configuration ---
    sd_threshold = float(os.getenv("SD_THRESHOLD", "2.0"))
    lookback_days = 30

    # --- Date range ---
    today = datetime.today()
    start_date = today - timedelta(days=lookback_days)

    print("=" * 60)
    print("MCB USD/MUR Forex Rate Monitor")
    print(f"Period: {start_date.strftime('%d-%b-%Y')} to {today.strftime('%d-%b-%Y')}")
    print(f"SD Threshold: {sd_threshold}")
    print("=" * 60)

    # --- Step 1: Download forex data ---
    print("\n[1] Downloading forex data from MCB...")
    success = functions.download_forex_data(start_date, today, "USD", "MUR")
    if not success:
        print("Failed to download data. Exiting.")
        return

    # --- Step 2: Parse and analyze ---
    print("\n[2] Analyzing exchange rates...")
    df = pd.read_excel('forex_data.xlsx', index_col=None, header=None)

    column_with_selling_tt = functions.find_column(df)
    if column_with_selling_tt is None:
        print("Could not find Selling TT column. Exiting.")
        return

    last_price = functions.get_lastprice(df, column_with_selling_tt)
    mean = functions.get_mean(df, column_with_selling_tt)
    std = functions.get_std(df, column_with_selling_tt)

    if last_price is None or mean is None or std is None:
        print("Could not calculate statistics. Exiting.")
        return

    # --- Step 3: Check deviation ---
    print("\n[3] Checking for significant deviation...")
    is_deviated, z_score, direction = functions.check_deviation(last_price, mean, std, sd_threshold)

    # --- Step 4: Send alert if deviated ---
    if is_deviated:
        print(f"\n[4] ALERT: Rate has deviated beyond {sd_threshold} SD! Sending Telegram notification...")
        functions.send_alert(last_price, mean, std, z_score, direction, sd_threshold)
    else:
        print(f"\n[4] Rate is within normal range (±{sd_threshold} SD). No alert needed.")
        print(f"    Current: {last_price:.2f} | Mean: {mean:.4f} | Z-Score: {z_score:.2f}")

    print("\n" + "=" * 60)
    print("Done.")


def test_telegram():
    """Send a test notification to verify Telegram is configured correctly."""
    print("Sending test notification to Telegram...")
    functions.send_test_notification()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test-telegram":
        test_telegram()
    else:
        main()
