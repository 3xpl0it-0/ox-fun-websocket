# things to know
in line 22 of ```tickers.py``` you can change the 10 to the amount you want to take.


the ```.env``` file has the urls for good practice even though its public not private, it's just ```OXFUN_API_URL=api.ox.fun``` and ```PHEMEX_WS_URL=wss://ws.phemex.com```.


```xxx_stream.py``` imports ```market_orders``` from ```xxx_tickers.py``` (```xxx_tickers.py``` imported and executed for ```market_orders``` to be kept in memory for the ```xxx_stream.py``` program). xxx is the exchange.


the csv file gets saved after the terminal is interrupted so when you're ready press control c on your keyboard in the terminal.
