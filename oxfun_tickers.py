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
    try:
        vol24 = float(i["volume24h"]) # this vol is in ox
    except:
        vol24 = "error"
    try:
        cvol24 = float(i["currencyVolume24h"]) # this vol is contracts traded
    except:
        cvol24 = "error"

    tickernvolume.append([i["marketCode"], vol24, cvol24])

top_x = sorted(tickernvolume, key=lambda x: x[1], reverse=True)[:10]

market_codes = []

for i in top_x:
    market_codes.append(i[0])

if __name__ == "__main__":
    print(market_codes)
    print("--------")
    print(top_x)