#app\app.py
import sys
import os

# Agregar el directorio raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from flask import Flask, render_template, request, jsonify  # Importa request y jsonify
from api.credit_notes import bp as credit_notes_bp
from api.invoices import bp as invoices_bp
from api.purchase_credit_notes import bp as purchase_credit_notes_bp
from api.purchase_invoices import bp as purchase_invoices_bp
from api.supplier import bp as supplier_bp
from api.stock_subgrupos import bp as stock_subgrupos_bp  
from api.profit import bp as profit_bp
from api.unidades_mensual_subgrupo import bp as ventas_compras_bp
from A_get_documentos_enteros.S_ejecutar_scripts import run_all_tasks_get_info, get_current_time
from B_features.S_ejecutar_features import run_all_tasks_features 

card_code = []

app = Flask(__name__)

# Registro de los blueprints de la API
app.register_blueprint(credit_notes_bp)
app.register_blueprint(invoices_bp)
app.register_blueprint(purchase_credit_notes_bp)
app.register_blueprint(purchase_invoices_bp)
app.register_blueprint(supplier_bp)
app.register_blueprint(stock_subgrupos_bp)
app.register_blueprint(profit_bp)
app.register_blueprint(ventas_compras_bp)

@app.route('/')
def dashboard():
    return render_template('dashboard2.html')

@app.route('/execute-tasks', methods=['POST'])
async def execute_tasks():
    if not request.is_json:
        return jsonify({"message": "La solicitud debe ser JSON."}), 400
    
    data = request.get_json()
    card_code = data.get('card_code', '')
    
    if not card_code:
        return jsonify({"message": "El card_code es obligatorio."}), 400

    start_time = get_current_time()

    try:
        # Ejecutar las tareas de forma asíncrona y pasar el card_code
        # Obtener los datos de la API
        await run_all_tasks_get_info(card_code)

        # Ejecutar la función que transforma y guarda los features
        feature_results = await run_all_tasks_features()

    except Exception as e:
        print(f"Error: {str(e)}")  # Para depuración
        return jsonify({
            "message": "Ocurrió un error durante la ejecución de las tareas.",
            "error": str(e)
        }), 500

    end_time = get_current_time()
    duration = end_time - start_time
    
    return jsonify({
        "message": f"Las tareas se ejecutaron en {duration}",
        "features": feature_results  # Retornar resultados de features
    })


if __name__ == '__main__':
    app.run(debug=True)
