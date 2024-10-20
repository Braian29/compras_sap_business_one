# app\api\stock_subgrupos.py
from flask import Blueprint, jsonify
import pandas as pd
import numpy as np

def load_csv_data(file_path):
    # Cargar los datos desde el archivo CSV
    data = pd.read_csv(file_path)
    
    # Reemplazar valores infinitos con None o un valor alternativo
    data.replace([np.inf, -np.inf], None, inplace=True)  # O usar 0 en lugar de None
    
    # Convertir a formato de diccionario para retornar como JSON
    return data.to_dict(orient='records')

# Crear un blueprint para la API de stock subgrupos
bp = Blueprint('stock_subgrupos', __name__)

# Cargar los datos al iniciar el módulo
stock_subgrupos = load_csv_data('data_outputs\stock_y_ventas_por_subgrupo.csv')  

@bp.route('/api/stock_subgrupos', methods=['GET'])
def api_stock_subgrupos():
    return jsonify(stock_subgrupos)
