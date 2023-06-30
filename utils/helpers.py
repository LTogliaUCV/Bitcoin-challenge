import pandas as pd

class RollingMeanCalculator:
    def __init__(self, df):
        self.df = df

    def calculate_rolling_mean(self):
        # Convert the 'date' column to datetime type
        self.df['date'] = pd.to_datetime(self.df['date'], format='%d-%m-%Y %H:%M:%S')

        # Set the 'date' column as the index of the DataFrame
        self.df.set_index('date', inplace=True)

        # Sort the DataFrame by the index in ascending order
        self.df.sort_index(inplace=True)

        # Create a rolling window with a window size of 5 days
        window = self.df.rolling(window='5D')

        # Aggregate the data by the window and calculate the mean value of 'value'
        result = window['price'].mean()

        return  result