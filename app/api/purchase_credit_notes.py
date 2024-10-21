#app\api\purchase_credit_notes.py 
from flask import Blueprint, jsonify
from .utils import load_csv_data

# Crear un blueprint para la API de purchase credit notes
bp = Blueprint('purchase_credit_notes', __name__)

# Cargar los datos al iniciar el módulo
purchase_credit_notes_summary = load_csv_data('data_outputs/purchasecreditnotes_summary.csv')

@bp.route('/api/purchase_credit_notes_summary', methods=['GET'])
def api_purchase_credit_notes_summary():
    return jsonify(purchase_credit_notes_summary)
