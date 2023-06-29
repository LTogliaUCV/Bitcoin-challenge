import requests
from datetime import datetime

class CoinGeckoAPI:
    

    def get_market_chart_data(self,coin, vs_currency, from_timestamp, to_timestamp, precision):
        url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range?vs_currency={vs_currency}&from={from_timestamp}&to={to_timestamp}&precision={precision}"
        
        print(url)
        headers = {}
        

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            for i in range(len(data["prices"])):
                timestamp = datetime.fromtimestamp(data["prices"][i][0] / 1000)
                data["prices"][i][0] = timestamp.strftime('%d-%m-%Y %H:%M:%S')
                data['market_caps'][i][0] = timestamp.strftime('%d-%m-%Y %H:%M:%S')
                data['total_volumes'][i][0] = timestamp.strftime('%d-%m-%Y %H:%M:%S')
            return data
        else:
            return None
            

   
    def get_coin_list(self):
        url = "https://api.coingecko.com/api/v3/coins/list"
        headers = {}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            return data
        else:
            return None