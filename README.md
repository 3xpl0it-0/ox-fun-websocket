# where stuff is
in line 22 of ```tickers.py``` you can change the 10 to the amount you want to take.


the ```.env``` file has the api url for good practice even though its public not private, it's just ```API_URL=api.ox.fun```.


```stream.py``` imports ```market_orders``` from ```tickers.py``` (```tickers.py``` imported and executed for ```market_orders``` to be kept in memory for the ```stream.py``` program).
