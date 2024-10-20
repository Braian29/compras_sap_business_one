# app/api/supplier.py 
from flask import Blueprint, jsonify
from .utils import load_json_data

bp = Blueprint('supplier', __name__)

supplier_data = load_json_data("data/supplier_data.json")  # Cargar los datos al iniciar el módulo

@bp.route('/api/supplier', methods=['GET'])
def api_supplier():
    return jsonify(supplier_data)
