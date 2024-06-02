import pandas as pd

class CSVProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def process_csv(self):
        data = pd.read_csv(self.input_file)
        data = data.dropna()
        data['combined_info'] = data.apply(
            lambda row: ', '.join([f"{col}: {row[col]}" for col in data.columns]),
            axis=1
        )
        data[['combined_info']].to_csv(self.output_file, index=False)

