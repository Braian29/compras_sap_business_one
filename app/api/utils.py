#app\api\utils.py 
import pandas as pd
import json
import math



def load_csv_data(file_path):
    """Carga datos desde un archivo CSV y los devuelve en formato de lista de diccionarios."""
    df = pd.read_csv(file_path)
    return df.to_dict(orient='records')


def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        # Iterate through the data to replace NaN values
        for supplier in data:
            if 'CurrentAccountBalance' in supplier and isinstance(supplier['CurrentAccountBalance'], float) and math.isnan(supplier['CurrentAccountBalance']):
                supplier['CurrentAccountBalance'] = 0  # or another default value
    return data

