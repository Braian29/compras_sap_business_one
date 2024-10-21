# app/api/profit.py
from flask import Blueprint, jsonify
import pandas as pd

def load_csv_data(file_path):
    """Carga los datos de un archivo CSV y los devuelve en formato dict (listo para JSON)."""
    df = pd.read_csv(file_path)
    return df.to_dict(orient='records')

# Crear un blueprint para la API de profit
bp = Blueprint('profit', __name__)



@bp.route('/api/profit_by_month', methods=['GET'])
def api_profit_by_month():
    # Cargar los datos de rentabilidad al iniciar el módulo
    profit_by_month = load_csv_data('data_outputs/profit_by_month.csv')
    return jsonify(profit_by_month)
