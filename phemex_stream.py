import asyncio
import json
import websockets
from dotenv import load_dotenv
import os
import time
from phemex_tickers import market_codes
import pandas as pd

load_dotenv()
ws_url = os.getenv('PHEMEX_WS_URL')

if not ws_url:
    raise ValueError("WS_URL is not set in environment variables.")

collected_data_l = []

async def subscribe_orderbook(ws, symbol):
    subscribe_msg = {
        "id": 1,
        "method": "orderbook.subscribe",
        "params": [symbol]
    }
    await ws.send(json.dumps(subscribe_msg))
    print(f"Subscribed to orderbook for {symbol}")

async def send_ping(ws):
        ping_msg = {
            "id": 1234,
            "method": "server.ping",
            "params": []
        }
        try:
            await ws.send(json.dumps(ping_msg))
            print("Ping sent")

        except Exception as e:
            print("Ping failed:", e)

async def wrap_up(symbol):
    while True:
        s = time.perf_counter()
        try:
            async with websockets.connect(ws_url, ping_interval=None) as ws:
                await subscribe_orderbook(ws, symbol)
                while ws.open:
                    response = await ws.recv()
                    res = json.loads(response)
                    if "symbol" in res:
                        collected_data_l.append([
                                res.get("sequence"),
                                res.get("timestamp"),
                                res.get("symbol"),
                                res["book"]["asks"][0][0] if res["book"]["asks"] else None,
                                res["book"]["asks"][0][1] if res["book"]["asks"] else None,
                                res["book"]["bids"][0][0] if res["book"]["bids"] else None,
                                res["book"]["bids"][0][1] if res["book"]["bids"] else None
                            ])
                    if time.perf_counter() - s >= 5:
                        await send_ping(ws)
                        s = time.perf_counter()
                    await asyncio.sleep(1)

        except Exception as e:
            print(f"error: {e}")
            await asyncio.sleep(3)

async def main():
    s = time.perf_counter()
    tasks = [asyncio.create_task(wrap_up(code)) for code in market_codes]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down gracefully (KeyboardInterrupt).")
    except Exception as e:
        print("Main error: {e}")
    finally:
        columns = [
            "sequence number",
            "asset",
            "time (from exchange)",
            "ask",
            "ask size",
            "bid",
            "bid size"
        ]

        collected_data = pd.DataFrame(collected_data_l, columns=columns)
        collected_data.to_csv(f"phemex_output start {collected_data["time (from exchange)"].iloc[0]} end {collected_data["time (from exchange)"].iloc[-1]}.csv", index=False)
        print("csv saved")