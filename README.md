# Btc finantial team challenge

Develop an automated and scalable process to obtain the average of each 5
days (moving average) of the price of bitcoin in the first quarter of 2022.


# Updating Bitcoin Prices in a Database

The scripts allows you to update Bitcoin prices in a SQLite3 database using the CoinGecko API.

## Requirements

- Python 3.x
- Install requirements.txt
- URL from  `CoinGeckoAPI`
- Create .env file using the env.example guide.
- You can change the dates, windows size , db name , table name using the .env file
## Usage

```python
python load_data_btc.py
python load_rolling_btc.py
```

## Next Step
- Create and pipeline using AWS Step functions or Airflow
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)