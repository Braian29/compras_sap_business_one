#app\api\purchase_invoices.py 
from flask import Blueprint, jsonify
from .utils import load_csv_data

# Crear un blueprint para la API de purchase invoices
bp = Blueprint('purchase_invoices', __name__)


@bp.route('/api/purchase_invoices_summary', methods=['GET'])
def api_purchase_invoices_summary():
    # Cargar los datos al iniciar el módulo
    purchase_invoices_summary = load_csv_data('data_outputs/purchaseinvoices_summary.csv')

    return jsonify(purchase_invoices_summary)
