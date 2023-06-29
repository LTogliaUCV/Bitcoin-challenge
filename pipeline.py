import pandas as pd
from utils.coin import CoinGeckoAPI
from utils.manager import BitcoinDatabase
from utils.helpers import  RollingMeanCalculator
# Instantiate the CoinGeckoAPI class
cg_api = CoinGeckoAPI()

# Define the input parameters
coin = "bitcoin"
vs_currency = "usd"
from_timestamp = 1641009600  
to_timestamp = 1651377599  
precision = 4               

# Call the get_market_chart_data() method to retrieve the market chart data
market_data = cg_api.get_market_chart_data(coin, vs_currency, from_timestamp, to_timestamp, precision)

# Extract the 'prices' data from the market data dictionary
data = market_data['prices']
print("teh data has ", len(data))

df_from_api_data = pd.DataFrame(data, columns=['date', 'price'])
# Create a new instance of the BitcoinDatabase class
btc_db = BitcoinDatabase('btc_data.db', 'btc_history_v2')

# Insert the market data into the table
btc_db.insert_data(df_from_api_data , 'btc_history_v2')

# Select and display the data from the table
results =btc_db.select_data('btc_history_v2')

# Create a RollingMeanCalculator object with the DataFrame
calculator = RollingMeanCalculator(results)

# Call the calculate_rolling_mean method on the RollingMeanCalculator object
result = calculator.calculate_rolling_mean()

# Print the result
print(result)