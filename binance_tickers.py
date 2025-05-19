import requests

def fetch_ticker_data():
    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        print("error fetching data:", error)

all_data = fetch_ticker_data()

tickernvolume = []

#print(all_data[1])

for i in all_data:
    try:
        vol24 = float(i["quoteVolume"]) # this vol is usdt
    except:
        vol24 = "error"
    try:
        cvol24 = float(i["volume"]) # this vol is contracts traded
    except:
        cvol24 = "error"

    tickernvolume.append([i["symbol"], vol24, cvol24])

top_x = sorted(tickernvolume, key=lambda x: x[1], reverse=True)[:10]

market_codes = []

k = 1
for i in top_x:
    market_codes.append([i[0], int(k)])
    k = k + 1

if __name__ == "__main__":
    print(market_codes)
    print("--------")
    print(top_x)