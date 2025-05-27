import asyncio
import json
import os
import pandas as pd
import websockets
from dotenv import load_dotenv
from binance_tickers import market_codes

load_dotenv()
ws_url = os.getenv("BINANCE_BASE_URL")

# single stream: /ws/<streamName>
# combined stream: /stream?streams=<streamName1>/<streamName2>/<streamName3>
# max 1024 at same time
# partial orderbook fastest latency option: <symbol>@depth<levels>@100ms , levels = 5, 10, 20

codes = []
for i in market_codes:
    codes.append(f"{i[0].lower()}@depth@100ms")

ws_url = ws_url+"/stream?streams="

for i in codes:
    ws_url = ws_url+i+"/"

ws_url=ws_url[:-1]

print(ws_url)

if not ws_url:
    raise ValueError("API_URL is not set in environment variables.")

collected_data_l = []

async def main():
    while True:
        try:
            async with websockets.connect(ws_url) as ws:
                while ws.open:

                    response = await ws.recv()
                    res = json.loads(response)
                    print(res)
                    if "data" in res:
                        collected_data_l.append([
                                res["data"].get("E"),
                                res["data"].get("s"),
                                res["data"].get("T"),
                                res["data"]["a"][0][0] if res["data"]["a"] else None,
                                res["data"]["a"][0][1] if res["data"]["a"] else None,
                                res["data"]["b"][-1][0] if res["data"]["b"] else None,
                                res["data"]["b"][-1][1] if res["data"]["b"] else None
                            ])
                        
        except Exception as e:
            print(f"error: {e}")
            await asyncio.sleep(3)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down gracefully (KeyboardInterrupt).")
    except Exception as e:
        print("Main error: {e}")
    finally:
        columns = [
            "event time",
            "asset",
            "transaction time",
            "ask",
            "ask size",
            "bid",
            "bid size"
        ]

        collected_data = pd.DataFrame(collected_data_l, columns=columns)
        collected_data.to_csv(f"binance_output start {collected_data["event time"].iloc[0]} end {collected_data["event time"].iloc[-1]}.csv", index=False)
        print("csv saved")
