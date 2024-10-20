#app\api\credit_notes.py 
from flask import Blueprint, jsonify
from .utils import load_csv_data

# Crear un blueprint para la API de credit notes
bp = Blueprint('credit_notes', __name__)

# Cargar los datos al iniciar el módulo
credit_notes_summary = load_csv_data('data_outputs/credit_notes_summary.csv')

@bp.route('/api/credit_notes_summary', methods=['GET'])
def api_credit_notes_summary():
    return jsonify(credit_notes_summary)
