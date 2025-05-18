import requests

def fetch_ticker_data():
    url = "https://api.phemex.com/md/ticker/24hr/all"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print('Error fetching ticker data:', error)

all_data = fetch_ticker_data()

tickernvolume = []

for i in all_data["result"]:
    tickernvolume.append([i["symbol"], i["turnover"], i["volume"]])

top_x = sorted(tickernvolume, key=lambda x: x[2], reverse=True)[:10]

market_codes = []

for i in top_x:
    market_codes.append(i[0])

if __name__ == "__main__":
    print(market_codes)