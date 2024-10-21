#app\api\credit_notes.py 
from flask import Blueprint, jsonify
from .utils import load_csv_data

# Crear un blueprint para la API de credit notes
bp = Blueprint('credit_notes', __name__)


@bp.route('/api/credit_notes_summary', methods=['GET'])
def api_credit_notes_summary():
    # Cargar los datos cada vez que se accede a la ruta
    credit_notes_summary = load_csv_data('data_outputs/creditnotes_summary.csv')
    return jsonify(credit_notes_summary)
