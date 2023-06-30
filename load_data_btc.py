import pandas as pd  # Importa la librería pandas para trabajar con dataframes
from utils.coin import CoinGeckoAPI  # Importa la clase CoinGeckoAPI de un módulo personalizado
from utils.manager import BitcoinDatabase  # Importa la clase BitcoinDatabase de un módulo personalizado


def main():
    # Crea una instancia de la clase CoinGeckoAPI
    cg_api = CoinGeckoAPI()

    # Obtiene una lista de todas las criptomonedas disponibles en CoinGecko
    coin_list = cg_api.get_coin_list()

    # Selecciona la criptomoneda a filtrar (en este caso Bitcoin)
    coint_to_filter = 'Bitcoin'

    # Filtra la lista de criptomonedas para obtener un diccionario de la criptomoneda seleccionada
    bitcoint_dic = [d for d in coin_list if d['name'] == coint_to_filter]

    # Obtiene el ID de la criptomoneda seleccionada
    coin = bitcoint_dic[0]['id']

    # Define los parámetros de entrada para la obtención de los datos de precios
    vs_currency = "usd"
    from_timestamp = 1641009600
    to_timestamp = 1651377599
    precision = 4

    # Obtiene los datos de precios de CoinGecko
    market_data = cg_api.get_market_chart_data(coin, vs_currency, from_timestamp, to_timestamp, precision)

    # Extrae la lista de precios y fechas de los datos obtenidos
    data = market_data['prices']

    # Convierte la lista de precios y fechas en un dataframe de pandas
    df_from_api_data = pd.DataFrame(data, columns=['date', 'price'])

    # Crea una instancia de la clase BitcoinDatabase
    btc_db = BitcoinDatabase('btc_database.db', "btc_history4")

    # Obtiene los datos de precios de Bitcoin almacenados en la base de datos
    btc_history_data = btc_db.select_data("btc_history4")

    # Obtiene la fecha más reciente en la que se registró un precio de Bitcoin en la base de datos
    date_max = list(btc_history_data.reset_index()['date'].agg(['max']).fillna(''))[0]

    # Agrega un índice al dataframe de precios de Bitcoin
    btc_history_data = btc_history_data.reset_index()

    # Filtra el dataframe de precios de CoinGecko para obtener solo los precios que aún no están en la base de datos
    filtered_df_to_load = df_from_api_data.loc[df_from_api_data['date'] > date_max]

    # Inserta los nuevos precios de Bitcoin en la base de datos
    if len(filtered_df_to_load):
        print(f"se insertan en db {len(filtered_df_to_load)} registros")
        btc_db.insert_data(filtered_df_to_load, "btc_history4")

        # Obtiene los datos de precios de Bitcoin almacenados en la base de datos después de la actualización
        btc_data_db = btc_db.select_data("btc_history4")
        count = len(btc_data_db)
        max_date_in_db = date_max = list(btc_data_db.reset_index()['date'].agg(['max']).fillna(''))[0]
        print(f"hay un  total de {count} de registros y la fecha mas reciente es {max_date_in_db}")

    # Si no hay nuevos precios de Bitcoin para insertar, imprime un mensaje indicando que la base de datos ya está actualizada
    else:
        print("already up tu date")
        count = len(btc_history_data)
        print(f"el dataset contiene  {count} registros")
        print(f"hay un  total de {count} de registros y la fecha mas reciente es {date_max}")


if __name__ == "__main__":
    main()