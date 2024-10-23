import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from flask import Flask, render_template, request, jsonify
from api.credit_notes import bp as credit_notes_bp
from api.invoices import bp as invoices_bp
from api.purchase_credit_notes import bp as purchase_credit_notes_bp
from api.purchase_invoices import bp as purchase_invoices_bp
from api.supplier import bp as supplier_bp
from api.stock_subgrupos import bp as stock_subgrupos_bp
from api.profit import bp as profit_bp
from api.unidades_mensual_subgrupo import bp as ventas_compras_bp


def serialize_dataframe(df):
    """Convierte un DataFrame a un formato JSON serializable"""
    if isinstance(df, pd.DataFrame):
        return df.to_dict(orient='records')
    return df

def serialize_features(features):
    """Serializa los resultados de features, manejando DataFrames y estructuras anidadas"""
    if isinstance(features, dict):
        return {k: serialize_features(v) for k, v in features.items()}
    elif isinstance(features, list):
        return [serialize_features(item) for item in features]
    elif isinstance(features, pd.DataFrame):
        return serialize_dataframe(features)
    return features

app = Flask(__name__)

# Registro de los blueprints
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
    from A_get_documentos_enteros.S_ejecutar_scripts import get_current_time, run_all_tasks_get_info
    from B_features.S_ejecutar_features import run_all_tasks_features

    if not request.is_json:
        return jsonify({"message": "La solicitud debe ser JSON."}), 400
    
    data = request.get_json()
    card_code = data.get('card_code', '')
    
    if not card_code:
        return jsonify({"message": "El card_code es obligatorio."}), 400

    start_time = get_current_time()
    
    try:
        # Ejecutar las tareas
        await run_all_tasks_get_info(card_code)
        feature_results = await run_all_tasks_features()
        
        # Serializar los resultados antes de enviarlos
        serialized_results = serialize_features(feature_results)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "message": "Ocurrió un error durante la ejecución de las tareas.",
            "error": str(e)
        }), 500

    end_time = get_current_time()
    duration = end_time - start_time

    return jsonify({
        "message": f"Las tareas se ejecutaron en {duration}",
        "features": serialized_results
    })

if __name__ == '__main__':
    app.run(debug=True)