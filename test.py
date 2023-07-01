import unittest
import os
from utils.coin import CoinGeckoAPI 
from load_data_btc import main, BitcoinDatabase

class TestMainScript(unittest.TestCase):

    def setUp(self):
        self.db_name = os.getenv("BTC_DB")
        self.table_btc_price_history = os.getenv("BTC_PRICE_TABLE")

    def test_main(self):
        # Test the main function in the script
        main()

        # Check that the database was updated correctly
        db = BitcoinDatabase(self.db_name, self.table_btc_price_history)
        btc_data_db = db.select_data(self.table_btc_price_history)
        count = len(btc_data_db)
        self.assertGreater(count, 0)  # Check that there is at least one row in the database


    def test_api_connection(self):
        # Test the connection to the CoinGecko API
        main()

        # Check that the API response was successful
        cg_api = CoinGeckoAPI()

        # Get all the coint list from CoinGecko
        coin_list = cg_api.get_coin_list()

        if coin_list:
            print("succesfull connection")

TestMainScript.test_api_connection("test")