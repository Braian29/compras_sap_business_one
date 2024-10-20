"""import json
import pandas as pd
from pathlib import Path

# Función para procesar documentos de ventas/compras y agrupar por mes
def process_documents(file_path, doc_type, output_file):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Almacenar los datos en listas para construir el DataFrame
    rows = []
    for doc in data:
        header = doc[doc_type]
        line = doc[f"{doc_type}/DocumentLines"]

        # Extraer la fecha y convertirla en formato datetime
        doc_date = pd.to_datetime(header["DocDate"], format='%Y-%m-%d')

        # Crear un registro con el mes, tipo de documento, cantidad y total
        rows.append({
            "Month": doc_date.strftime('%Y-%m'),
            "DocType": doc_type,
            "Quantity": line["Quantity"],
            "LineTotal": line["LineTotal"]
        })

    # Crear un DataFrame
    df = pd.DataFrame(rows)

    # Agrupar por mes
    summary = df.groupby('Month').agg({'Quantity': 'sum', 'LineTotal': 'sum'}).reset_index()

    # Guardar los resultados en un archivo CSV
    summary.to_csv(output_file, index=False)
    print(f"Datos procesados guardados en: {output_file}")

# Procesar cada tipo de documento
output_folder = Path('data_outputs')
output_folder.mkdir(exist_ok=True)

# Procesar Notas de Crédito de Venta
process_documents('data/CreditNotes.json', 'CreditNotes', output_folder / 'credit_notes_summary.csv')

# Procesar Facturas de Venta
process_documents('data/Invoices.json', 'Invoices', output_folder / 'invoices_summary.csv')

# Procesar Notas de Crédito de Compra
process_documents('data/PurchaseCreditNotes.json', 'PurchaseCreditNotes', output_folder / 'purchase_credit_notes_summary.csv')

# Procesar Facturas de Compra
process_documents('data/PurchaseInvoices.json', 'PurchaseInvoices', output_folder / 'purchase_invoices_summary.csv')



import pandas as pd

# Leer los archivos CSV generados
credit_notes = pd.read_csv('data_outputs/credit_notes_summary.csv')
invoices = pd.read_csv('data_outputs/invoices_summary.csv')
purchase_credit_notes = pd.read_csv('data_outputs/purchase_credit_notes_summary.csv')
purchase_invoices = pd.read_csv('data_outputs/purchase_invoices_summary.csv')

# Asegurarse de que todos los meses estén presentes en ventas y compras
all_months = pd.concat([invoices['Month'], purchase_invoices['Month'], credit_notes['Month'], purchase_credit_notes['Month']]).unique()

# Crear un DataFrame para asegurarse de que todos los meses están representados
months_df = pd.DataFrame(all_months, columns=['Month'])

# Combinar ventas (invoices - credit notes)
# Agrupamos por mes y calculamos las ventas netas, manejando los NaN (falta de datos)
sales = months_df.merge(invoices, on='Month', how='left').merge(credit_notes, on='Month', how='left', suffixes=('_invoice', '_creditnote'))
sales['LineTotal_invoice'] = sales['LineTotal_invoice'].fillna(0)  # Si no hay facturas, son 0
sales['LineTotal_creditnote'] = sales['LineTotal_creditnote'].fillna(0)  # Si no hay notas de crédito, son 0
sales['NetSales'] = sales['LineTotal_invoice'] - sales['LineTotal_creditnote']

# Combinar compras (purchase invoices - purchase credit notes)
# Agrupamos por mes y calculamos las compras netas, manejando los NaN
purchases = months_df.merge(purchase_invoices, on='Month', how='left').merge(purchase_credit_notes, on='Month', how='left', suffixes=('_invoice', '_creditnote'))
purchases['LineTotal_invoice'] = purchases['LineTotal_invoice'].fillna(0)  # Si no hay facturas de compra, son 0
purchases['LineTotal_creditnote'] = purchases['LineTotal_creditnote'].fillna(0)  # Si no hay notas de crédito de compra, son 0
purchases['NetPurchases'] = purchases['LineTotal_invoice'] - purchases['LineTotal_creditnote']

# Combinar ventas y compras para calcular la rentabilidad
profit = sales[['Month', 'NetSales']].merge(purchases[['Month', 'NetPurchases']], on='Month')
profit['Profit'] = profit['NetSales'] - profit['NetPurchases']

# Guardar la rentabilidad mensual en un archivo CSV
output_csv = 'data_outputs/profit_by_month.csv'
profit.to_csv(output_csv, index=False)
print(f"Archivo de rentabilidad mensual guardado en: {output_csv}")
"""

import json
import pandas as pd
from pathlib import Path

# Función para cargar datos desde un archivo JSON
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Función para procesar documentos de ventas/compras y agrupar por mes
def process_documents(file_path, doc_type):
    data = load_json(file_path)

    # Almacenar los datos en listas para construir el DataFrame
    rows = []
    for doc in data:
        header = doc[doc_type]
        line = doc[f"{doc_type}/DocumentLines"]

        # Extraer la fecha y convertirla en formato datetime
        doc_date = pd.to_datetime(header["DocDate"], format='%Y-%m-%d')

        # Crear un registro con el mes, tipo de documento, cantidad y total
        rows.append({
            "Month": doc_date.strftime('%Y-%m'),
            "DocType": doc_type,
            "Quantity": line["Quantity"],
            "LineTotal": line["LineTotal"]
        })

    # Crear un DataFrame y agrupar por mes
    df = pd.DataFrame(rows)
    summary = df.groupby('Month').agg({'Quantity': 'sum', 'LineTotal': 'sum'}).reset_index()
    
    return summary

# Función para procesar todos los tipos de documentos
def process_all_documents(output_folder):
    output_folder.mkdir(exist_ok=True)
    summaries = {}

    # Procesar cada tipo de documento
    doc_types = {
        'CreditNotes': 'data/CreditNotes.json',
        'Invoices': 'data/Invoices.json',
        'PurchaseCreditNotes': 'data/PurchaseCreditNotes.json',
        'PurchaseInvoices': 'data/PurchaseInvoices.json'
    }

    for doc_type, file_path in doc_types.items():
        summary = process_documents(file_path, doc_type)
        summaries[doc_type] = summary
        summary.to_csv(output_folder / f'{doc_type.lower()}_summary.csv', index=False)
        print(f"Datos procesados guardados en: {output_folder}/{doc_type.lower()}_summary.csv")

    return summaries

# Función para combinar resúmenes de ventas y compras
def combine_sales_and_purchases(summaries):
    # Leer resúmenes
    invoices = summaries['Invoices']
    credit_notes = summaries['CreditNotes']
    purchase_invoices = summaries['PurchaseInvoices']
    purchase_credit_notes = summaries['PurchaseCreditNotes']

    # Asegurarse de que todos los meses estén presentes en ventas y compras
    all_months = pd.concat([invoices['Month'], purchase_invoices['Month'], credit_notes['Month'], purchase_credit_notes['Month']]).unique()
    months_df = pd.DataFrame(all_months, columns=['Month'])

    # Combinar ventas
    sales = months_df.merge(invoices, on='Month', how='left').merge(credit_notes, on='Month', how='left', suffixes=('_invoice', '_creditnote'))
    sales['LineTotal_invoice'] = sales['LineTotal_invoice'].fillna(0)
    sales['LineTotal_creditnote'] = sales['LineTotal_creditnote'].fillna(0)
    sales['NetSales'] = sales['LineTotal_invoice'] - sales['LineTotal_creditnote']

    # Combinar compras
    purchases = months_df.merge(purchase_invoices, on='Month', how='left').merge(purchase_credit_notes, on='Month', how='left', suffixes=('_invoice', '_creditnote'))
    purchases['LineTotal_invoice'] = purchases['LineTotal_invoice'].fillna(0)
    purchases['LineTotal_creditnote'] = purchases['LineTotal_creditnote'].fillna(0)
    purchases['NetPurchases'] = purchases['LineTotal_invoice'] - purchases['LineTotal_creditnote']

    # Calcular rentabilidad
    profit = sales[['Month', 'NetSales']].merge(purchases[['Month', 'NetPurchases']], on='Month')
    profit['Profit'] = profit['NetSales'] - profit['NetPurchases']

    return profit

# Función principal para ejecutar el procesamiento
def process_data_profit():
    output_folder = Path('data_outputs')
    summaries = process_all_documents(output_folder)
    profit = combine_sales_and_purchases(summaries)

    # Guardar la rentabilidad mensual en un archivo CSV
    output_csv = output_folder / 'profit_by_month.csv'
    profit.to_csv(output_csv, index=False)
    print(f"Archivo de rentabilidad mensual guardado en: {output_csv}")

# Descomentar para ejecutar el procesamiento
process_data_profit()
