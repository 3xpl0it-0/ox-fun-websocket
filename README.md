# things to know
in line 22 of ```tickers.py``` you can change the 10 to the amount you want to take.


the ```.env``` file has the api url for good practice even though its public not private, it's just ```API_URL=api.ox.fun```.


```stream.py``` imports ```market_orders``` from ```tickers.py``` (```tickers.py``` imported and executed for ```market_orders``` to be kept in memory for the ```stream.py``` program).


the csv file gets saved after the terminal is interrupted so when you're ready press control c on your keyboard in the terminal.
