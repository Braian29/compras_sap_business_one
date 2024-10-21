# app/api/ventas_compras.py
from flask import Blueprint, jsonify
import pandas as pd

def load_csv_data(file_path):
    """Carga los datos de un archivo CSV y los devuelve en formato dict (listo para JSON)."""
    df = pd.read_csv(file_path)
    # Convertir la columna 'Mes' a formato de fecha
    df['Mes'] = pd.to_datetime(df['Mes'])
    # Convertir las fechas a formato string para que sean serializables en JSON
    df['Mes'] = df['Mes'].dt.strftime('%Y-%m-%d')
    return df.to_dict(orient='records')

# Crear un blueprint para la API de ventas y compras
bp = Blueprint('ventas_compras', __name__)



@bp.route('/api/ventas_compras_por_subgrupo', methods=['GET'])
def api_ventas_compras_por_subgrupo():
    # Cargar los datos de ventas y compras al iniciar el módulo
    ventas_compras_por_subgrupo = load_csv_data('data_outputs/ventas_compras_por_subgrupo.csv')
    return jsonify(ventas_compras_por_subgrupo)