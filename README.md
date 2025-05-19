# things to know
in ```xxx_tickers.py``` where xxx is the exchange, in the line ```top_x = sorted(tickernvolume, key=lambda x: x[1], reverse=True)[:10]``` you can change the 10 to the amount you want to take.


the ```.env``` file has the urls for good practice even though its public not private, it's just ```OXFUN_API_URL=api.ox.fun```, ```PHEMEX_WS_URL=wss://ws.phemex.com``` and ```BINANCE_BASE_URL=wss://fstream.binance.com```.


```xxx_stream.py``` imports ```market_orders``` from ```xxx_tickers.py``` (```xxx_tickers.py``` imported and executed for ```market_orders``` to be kept in memory for the ```xxx_stream.py``` program).


the csv file gets saved after the terminal is interrupted so when you're ready press control c on your keyboard in the terminal.
