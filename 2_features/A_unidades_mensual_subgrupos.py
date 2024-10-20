import json
from collections import defaultdict
from datetime import datetime
import pandas as pd

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='iso-8859-1') as file:
            return json.load(file)

def process_document(docs, is_purchase, is_credit):
    result = {}
    for doc in docs:
        doc_header = list(doc.keys())[0]  # 'Invoices', 'CreditNotes', etc.
        doc_lines = list(doc.values())[1]  # 'Invoices/DocumentLines', etc.
        
        item_code = doc_lines['ItemCode']
        quantity = doc_lines['Quantity']
        doc_date = datetime.strptime(doc[doc_header]['DocDate'], '%Y-%m-%d')
        month_key = f"{doc_date.year}-{doc_date.month:02d}"
        
        if item_code not in result:
            result[item_code] = defaultdict(lambda: {'purchase': 0, 'sale': 0})
        
        if is_purchase:
            result[item_code][month_key]['purchase'] += quantity if not is_credit else -quantity
        else:
            result[item_code][month_key]['sale'] += quantity if not is_credit else -quantity
    
    return result

def merge_results(results):
    merged = defaultdict(lambda: defaultdict(lambda: {'purchase': 0, 'sale': 0}))
    for result in results:
        for item_code, months in result.items():
            for month, data in months.items():
                merged[item_code][month]['purchase'] += data['purchase']
                merged[item_code][month]['sale'] += data['sale']
    return merged

def get_subgroup(item_code, items_data):
    for item in items_data:
        if 'ItemCode' in item and item['ItemCode'] == item_code:
            return item.get('U_SC_Grupo2', 'Unknown')
    return 'Unknown'

def create_dataframe(final_result):
    data = []
    for subgroup, months in final_result.items():
        for month, values in months.items():
            data.append({
                'Subgrupo': subgroup,
                'Mes': month,
                'Unidades Compradas': values['purchase'],
                'Unidades Vendidas': values['sale']
            })
    
    df = pd.DataFrame(data)
    df['Mes'] = pd.to_datetime(df['Mes'])
    df = df.sort_values(['Subgrupo', 'Mes'])
    return df

def process_unidades_subgrupo_meses():
    # Cargar datos
    items = load_json('data/items.json')
    invoices = load_json('data/Invoices.json')
    credit_notes = load_json('data/CreditNotes.json')
    purchase_invoices = load_json('data/PurchaseInvoices.json')
    purchase_credit_notes = load_json('data/PurchaseCreditNotes.json')

    # Procesar documentos
    results = [
        process_document(invoices, False, False),
        process_document(credit_notes, False, True),
        process_document(purchase_invoices, True, False),
        process_document(purchase_credit_notes, True, True)
    ]

    # Combinar resultados
    merged_results = merge_results(results)

    # Agrupar por subgrupo
    final_result = defaultdict(lambda: defaultdict(lambda: {'purchase': 0, 'sale': 0}))
    for item_code, months in merged_results.items():
        subgroup = get_subgroup(item_code, items)
        for month, data in months.items():
            final_result[subgroup][month]['purchase'] += data['purchase']
            final_result[subgroup][month]['sale'] += data['sale']

    # Crear DataFrame
    df = create_dataframe(final_result)

    # Guardar DataFrame como CSV
    df.to_csv('data_outputs/ventas_compras_por_subgrupo.csv', index=False)

    # Mostrar las primeras filas del DataFrame
    print(df)

if __name__ == "__main__":
    process_unidades_subgrupo_meses()