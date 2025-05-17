# format: <BASE>-<QUOTE>-SWAP-LIN

import requests

def fetch_ticker_data():
    url = f'https://api.ox.fun/v3/tickers'

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print('Error fetching ticker data:', error)

all_data = fetch_ticker_data()

tickernvolume = []

for i in all_data["data"]:
    tickernvolume.append([i["marketCode"], i["volume24h"], i["currencyVolume24h"]])

top_x = sorted(tickernvolume, key=lambda x: x[2], reverse=True)[:10]

market_codes = []

for i in top_x:
    market_codes.append(i[0])
