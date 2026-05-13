# MCB USD/MUR Daily Forex Rate Monitor

Monitors the USD to MUR exchange rate from [MCB Mauritius](https://mcb.mu/tools-calculators/download-daily-rates) and sends Telegram alerts when:
- The rate deviates significantly from its 30-day average (standard deviation alert)
- The bank spread drops below a configured threshold (spread alert)

## How It Works

1. Downloads the last 30 days of USD/MUR selling TT rates from MCB's API
2. Fetches the real-time mid-market USD/MUR rate (free API, no key needed)
3. Calculates mean, standard deviation, and Z-score for the MCB rate
4. Calculates the bank spread: `(MCB Selling TT - Market Rate) / Market Rate × 100`
5. Sends Telegram alerts with human-readable rarity context if thresholds are breached

## Alerts

### Rate Deviation Alert
Triggers when the MCB rate moves beyond a configured number of standard deviations from the 30-day mean. Includes a rarity scale:

| Z-Score | Rarity |
|---------|--------|
| < 0.5 | 🟢 Very common (most days) |
| 0.5–1.0 | 🟢 Normal (~1 in 3 days) |
| 1.0–1.5 | 🟡 Uncommon (~1 in 7 days) |
| 1.5–2.0 | 🟠 Unusual (~1 in 20 days) |
| 2.0–2.5 | 🔴 Rare (~1 in 2 months) |
| 2.5–3.0 | 🔴 Very rare (~1 in 6 months) |
| > 3.0 | ⚫ Extremely rare (<1 in a year) |

### Spread Alert
Triggers when the MCB bank spread drops below the configured threshold. Includes a rarity scale based on 5+ years of historical data (2020–2026, ~1765 data points):

| Spread | Rarity |
|--------|--------|
| < 0.5% | ⚫ Unicorn (<0.1% of days) |
| 0.5–1.0% | 🔴 Extremely rare (~2% of days) |
| 1.0–1.5% | 🔴 Very rare (~6% of days) |
| 1.5–2.0% | 🟠 Rare (~10% of days) |
| 2.0–2.5% | 🟡 Uncommon (~15% of days) |
| 2.5–3.0% | 🟡 Below average (~22% of days) |
| 3.0–3.5% | 🟢 Normal — lower half |
| 3.5–4.0% | 🟢 Normal — typical (historical avg: 3.48%) |
| 4.0–4.5% | 🟢 Above average |
| > 4.5% | 📈 High spread |

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file (or set as GitHub Secrets):

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
SD_THRESHOLD=2.0
SPREAD_THRESHOLD=2.0
```

### 3. Telegram setup

1. Message [@BotFather](https://t.me/BotFather) → `/newbot` → copy the token
2. Send any message to your new bot
3. Visit `https://api.telegram.org/bot<TOKEN>/getUpdates` → grab the `chat_id`

### 4. Test Telegram

```bash
python main.py --test-telegram
```

### 5. Run the monitor

```bash
python main.py
```

## GitHub Actions (Automated Daily Run)

The workflow runs automatically at **09:30 Mauritius time (05:30 UTC)** Monday–Friday (MCB uploads rates ~08:55–09:05 MUT).

### Setup

1. Push to GitHub
2. Go to repo → **Settings → Secrets and variables → Actions**
3. Add **Secrets**: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
4. Add **Variables** (optional): `SD_THRESHOLD` (default: 2.0), `SPREAD_THRESHOLD` (default: 1.0)

You can also trigger manually from the Actions tab → "Run workflow".

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SD_THRESHOLD` | 2.0 | Z-score threshold for rate deviation alerts |
| `SPREAD_THRESHOLD` | 1.0 | Spread % below which to trigger alerts |

### SD Threshold Guide

The `SD_THRESHOLD` controls how sensitive the rate deviation alert is:

| Threshold | Sensitivity | Meaning |
|-----------|-------------|---------|
| 1.5 | High | Alerts on ~13% of days (more frequent) |
| 2.0 | Medium (recommended) | Alerts on ~5% of days |
| 2.5 | Low | Alerts on ~1% of days (rare, big moves only) |

Based on recent data, 1 SD ≈ 0.31 MUR, so a 2.0 SD threshold triggers when the rate moves ±0.63 MUR from the 30-day average.

### Spread Threshold Guide

The `SPREAD_THRESHOLD` controls when you get alerted about low bank spreads (good buying opportunities). Based on historical data (2020–2026):

| Threshold | Sensitivity | How often it triggers |
|-----------|-------------|----------------------|
| 1.0% | Very low | ~2% of days — only the rarest deals |
| 1.5% | Low | ~6% of days — about once a month |
| 2.0% | Medium (recommended) | ~10% of days — a few times a month |
| 2.5% | High | ~15% of days — roughly weekly |
| 3.0% | Very high | ~22% of days — frequent alerts |

Historical average (data since 2020) spread is 3.48%. Anything below 2% is genuinely unusual and worth paying attention to.

## Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point — download → analyze → alert |
| `functions.py` | Core logic (download, stats, spread, Telegram, rarity scales) |
| `modules.py` | Shared imports |
| `.env` | Local configuration (not committed) |
| `.github/workflows/forex-monitor.yml` | GitHub Actions scheduled workflow |
| `MCBSpreadData.csv` | Historical spread data (2020–2026) used to calibrate rarity scale |
| `forex_data.xlsx` | Downloaded rate data (regenerated each run) |
