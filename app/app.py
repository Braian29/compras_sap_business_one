from flask import Flask, render_template
from api.credit_notes import bp as credit_notes_bp
from api.invoices import bp as invoices_bp
from api.purchase_credit_notes import bp as purchase_credit_notes_bp
from api.purchase_invoices import bp as purchase_invoices_bp
from api.supplier import bp as supplier_bp
from api.stock_subgrupos import bp as stock_subgrupos_bp  
from api.profit import bp as profit_bp
from api.unidades_mensual_subgrupo import bp as ventas_compras_bp

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



if __name__ == '__main__':
    app.run(debug=True)
