import os
import pandas as pd
from dotenv import load_dotenv
from utils.coin import CoinGeckoAPI  
from utils.manager import BitcoinDatabase  

load_dotenv()

db_name = os.getenv("BTC_DB")
table_btc_price_history = os.getenv("BTC_PRICE_TABLE")
table_rolling_price_history = os.getenv("ROLLING_PRICE_TABLE")
bitcoin_name = os.getenv("COIN_BTC_NAME")
vs_currency= os.getenv("VS_CURRENCY")
from_timestamp = os.getenv("FROM_DATE")
to_timestamp = os.getenv("TO_DATE")
precision =os.getenv("PRECISION")


def main():
    # Init  the CoinGeckoAPI class
    cg_api = CoinGeckoAPI()

    # Get all the coint list from CoinGecko
    coin_list = cg_api.get_coin_list()
 
    # Choose the coin to filter (our case bitcoin)
    coint_to_filter = bitcoin_name
 
    # Filter list of dict from the api response
    bitcoint_dic = [d for d in coin_list if d['name'] == coint_to_filter]
    
    # Getting the coin id 
    coin = bitcoint_dic[0]['id']
 
    # Get the prices from the given timestamps
    market_data = cg_api.get_market_chart_data(coin, vs_currency, from_timestamp, to_timestamp, precision)

    # Select the prices from the dates
    data = market_data['prices']

    # Formating to pandas
    df_from_api_data = pd.DataFrame(data, columns=['date', 'price'])

    # Init the db
    btc_db = BitcoinDatabase(db_name, table_btc_price_history)

    # Get the data currently in the db
    btc_history_data = btc_db.select_data(table_btc_price_history)

    #  the most recent date into the db
    date_max = list(btc_history_data.reset_index()['date'].agg(['max']).fillna(''))[0]

    # Reset the index
    btc_history_data = btc_history_data.reset_index()

    # Filter by the max date to obtain values that are not in the database
    filtered_df_to_load = df_from_api_data.loc[df_from_api_data['date'] > date_max]

    # Insert the new values into the db
    if len(filtered_df_to_load):
        print(f"se insertan en db {len(filtered_df_to_load)} registros")
        btc_db.insert_data(filtered_df_to_load,  table_btc_price_history)

        # Check the db with the update
        btc_data_db = btc_db.select_data(table_btc_price_history)
        count = len(btc_data_db)
        max_date_in_db = date_max = list(btc_data_db.reset_index()['date'].agg(['max']).fillna(''))[0]
        print(f"hay un  total de {count} de registros y la fecha mas reciente es {max_date_in_db}")

    # If there are no new Bitcoin prices to insert, it prints a message indicating that the database is already up to date.
    else:
        print("already up tu date")
        count = len(btc_history_data)
        print(f"el dataset contiene  {count} registros")
        print(f"hay un  total de {count} de registros y la fecha mas reciente es {date_max}")


if __name__ == "__main__":
    main()