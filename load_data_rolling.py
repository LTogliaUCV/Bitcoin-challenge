from utils.manager import BitcoinDatabase
from utils.helpers import RollingMeanCalculator
from utils.manager import RollingMeanDatabase


def main():
    # Crear una instancia de la clase BitcoinDatabase para obtener los datos de precios de Bitcoin
    btc_db = BitcoinDatabase('btc_database.db', "btc_history4")

    # Obtener los datos de precios de Bitcoin de la base de datos y agregar un índice al dataframe
    btc_history_data = btc_db.select_data("btc_history4")
    btc_history_data = btc_history_data.reset_index()

    # Crear un objeto RollingMeanCalculator con el dataframe y calcular la media móvil
    calculator = RollingMeanCalculator(btc_history_data)
    result = calculator.calculate_rolling_mean()

    # Convertir la serie resultante en un DataFrame y renombrar las columnas
    rolling = result.to_frame()
    rolling.reset_index(inplace=True)
    rolling = rolling.rename(columns={'date': 'date'})
    rolling = rolling.rename(columns={'price': 'mean_value_price'})
    
    # Convertir la columna 'date' de datetime a una cadena en formato 'DD-MM-YYYY HH:MM:SS'
    rolling['date'] = rolling['date'].apply(lambda x: x.strftime('%d-%m-%Y %H:%M:%S'))

    # Crear una instancia de la clase RollingMeanDatabase para insertar los datos de la media móvil en la base de datos
    rolling_mean_db = RollingMeanDatabase('btc_database.db', 'rolling_mean_v10')

    # Seleccionar los datos de la media móvil de la base de datos y obtener la fecha más reciente
    rolling_history_data = rolling_mean_db.select_data('rolling_mean_v10')
    rolling_history_data = rolling_history_data.reset_index()
    date_max = list(rolling_history_data.reset_index()['date'].agg(['max']).fillna(''))[0]

    # Filtrar los nuevos registros a insertar en la base de datos
    filtered_df_to_load = rolling.loc[rolling['date'] > date_max]

    if len(filtered_df_to_load):
        # Insertar los nuevos registros en la base de datos y mostrar algunos detalles
        print(f"Se insertan en la base de datos {len(filtered_df_to_load)} registros")
        rolling_mean_db.insert_data(filtered_df_to_load, "rolling_mean_v10")
        rolling_data_db = rolling_mean_db.select_data("rolling_mean_v10")
        count = len(rolling_data_db)
        max_date_in_db = list(rolling_data_db.reset_index()['date'].agg(['max']).fillna(''))[0]
        print(f"Con el insert hay un total de {count} registros y la fecha más reciente es {max_date_in_db}")
    else:
        # No hay nuevos registros para insertar en la base de datos y mostrar algunos detalles
        print("Ya se encuentra actualizada")
        count = len(rolling_history_data)
        print(f"El dataset contiene {count} registros")
        print(f"Hay un total de {count} registros y la fecha más reciente es {date_max}")


if __name__ == "__main__":
    main()