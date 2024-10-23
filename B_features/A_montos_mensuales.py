#B_features\A_profit_montos_mensual.py
import json
import pandas as pd
from pathlib import Path




def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


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
def process_all_documents():
    output_folder = Path('data_outputs')
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

process_all_documents()