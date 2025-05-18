import requests

def fetch_ticker_data():
    url = "https://api.phemex.com/md/v3/ticker/24hr/all"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print('Error fetching ticker data:', error)

all_data = fetch_ticker_data()

tickernvolume = []

for i in all_data["result"]:
    try:
        vol24 = float(i["volumeRq"]) # this vol is contracts traded
    except:
        vol24 = "error"
    try:
        cvol24 = float(i["turnoverRv"]) # this vol is dollars traded
    except:
        cvol24 = "error"

    tickernvolume.append([i["symbol"], vol24, cvol24])

top_x = sorted(tickernvolume, key=lambda x: x[2], reverse=True)[:10]

market_codes = []

k = 1
for i in top_x:
    market_codes.append([i[0], int(k)])
    k = k + 1

if __name__ == "__main__":
    print(market_codes)
    print("------")
    print(top_x)