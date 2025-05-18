import asyncio
import websockets
import os
import json
import logging
from dotenv import load_dotenv
import pandas as pd
from tickers import market_codes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
api_url = os.getenv('API_URL')

collected_data_l = []

if not api_url:
    raise ValueError("API_URL is not set in environment variables.")

async def get_order_book_info(market_code):
    while True:
        try:
            async with websockets.connect(f"wss://{api_url}/v2/websocket") as websocket:
                while websocket.open:
                    response = await websocket.recv()
                    res = json.loads(response)

                    if res.get("success") is False:
                        logger.warning(res)
                        break

                    if "nonce" in res:
                        await websocket.send(json.dumps({
                            "op": "subscribe",
                            "tag": 103,
                            "args": [f"depthL25:{market_code}"]
                        }))
                    if "data" in res:
                        collected_data_l.append([
                            res["data"]["seqNum"],
                            res["data"]["marketCode"],
                            res["data"]["timestamp"],
                            res["data"]["asks"][0][0],
                            res["data"]["asks"][0][1],
                            res["data"]["bids"][0][0],
                            res["data"]["bids"][0][1]
                        ])
                        
                        logger.info(res["data"])
                    await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            await asyncio.sleep(3)

async def main():
    tasks = [asyncio.create_task(get_order_book_info(code)) for code in market_codes]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully (KeyboardInterrupt).")
    except Exception as e:
        logger.error(f"Main error: {e}")
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
        collected_data.to_csv(f"oxfun_output start {collected_data["time (from exchange)"].iloc[0]} end {collected_data["time (from exchange)"].iloc[-1]}.csv", index=False)
        print("csv saved")
