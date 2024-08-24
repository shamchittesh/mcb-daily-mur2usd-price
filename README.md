# mcb-daily-mur2usd-price
Tracks MCB daily MUR to USD trading price movement's standard deviation and push notifications to a telegram channel.

- python3 -m venv .venv
- source .venv/bin/activate
- python3 -m pip install -r requirements.txt

# Goals
- Find a way to get the rates from https://mcb.mu/tools-calculators/download-daily-rates
- Calculate the standard deviation for the price action
- Trigger a test notifications to telegram
- Find a suitable SD value and factor it in the code