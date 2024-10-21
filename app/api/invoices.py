#app\api\invoices.py 
from flask import Blueprint, jsonify
from .utils import load_csv_data

# Crear un blueprint para la API de invoices
bp = Blueprint('invoices', __name__)



@bp.route('/api/invoices_summary', methods=['GET'])
def api_invoices_summary():
    # Cargar los datos al iniciar el módulo
    invoices_summary = load_csv_data('data_outputs/invoices_summary.csv')
    return jsonify(invoices_summary)
