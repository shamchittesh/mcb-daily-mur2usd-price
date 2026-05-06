# MCB USD/MUR Daily Forex Rate Monitor

Monitors the USD to MUR exchange rate from [MCB Mauritius](https://mcb.mu/tools-calculators/download-daily-rates) and sends Telegram alerts when the rate deviates significantly from its 30-day average.

## How It Works

1. Downloads the last 30 days of USD/MUR selling TT rates from MCB's API
2. Calculates the mean and standard deviation of the rates
3. Computes a Z-score for the latest rate
4. If the Z-score exceeds the configured threshold, sends a Telegram alert

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Telegram

1. Create a bot via [@BotFather](https://t.me/BotFather) on Telegram
2. Send any message to your new bot
3. Get your chat ID by visiting: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Update `.env`:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
SD_THRESHOLD=2.0
```

### 3. Test Telegram

```bash
python main.py --test-telegram
```

### 4. Run the monitor

```bash
python main.py
```

## SD Threshold Guide

The `SD_THRESHOLD` in `.env` controls alert sensitivity:

| Threshold | Sensitivity | Meaning |
|-----------|-------------|---------|
| 1.5 | High | Alerts on ~13% of days (more frequent) |
| 2.0 | Medium (recommended) | Alerts on ~5% of days |
| 2.5 | Low | Alerts on ~1% of days (rare, big moves only) |

Based on recent data, 1 SD ≈ 0.31 MUR, so a 2.0 SD threshold triggers when the rate moves ±0.63 MUR from the 30-day average.

## Automation (Cron)

To run daily at 10:00 AM:

```bash
crontab -e
# Add:
0 10 * * * cd /path/to/project && /path/to/.venv/bin/python main.py
```

## Files

- `main.py` — Entry point, orchestrates download → analysis → alert
- `functions.py` — Core logic (download, stats, Telegram)
- `modules.py` — Shared imports
- `.env` — Configuration (bot token, chat ID, threshold)
- `forex_data.xlsx` — Downloaded rate data (regenerated each run)
