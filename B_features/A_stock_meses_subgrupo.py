import json
import pandas as pd
from datetime import datetime, timedelta

def load_json_data(file_path):
    """Carga datos de un archivo JSON."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_subgroup_dict(sub_grupos_data):
    """Crea un diccionario para mapear los códigos de subgrupo a nombres."""
    return {subgrupo['Code']: subgrupo['Name'] for subgrupo in sub_grupos_data}

def process_current_stock(items_data):
    """Procesa el stock actual y devuelve un DataFrame agrupado por subgrupo."""
    items = []
    for item in items_data:
        sub_group_code = item.get('U_SC_Grupo2', None)
        sub_group_code = sub_group_code.zfill(3) if sub_group_code else None
        for warehouse in item.get('ItemWarehouseInfoCollection', []):
            stock = warehouse.get('InStock', 0)
            items.append({
                'SubGroupCode': sub_group_code,
                'Stock': stock
            })

    stock_df = pd.DataFrame(items)
    return stock_df.groupby(['SubGroupCode']).agg({'Stock': 'sum'}).reset_index()

def process_sold_units(invoices_data):
    """Procesa las unidades vendidas en el último mes y devuelve un DataFrame agrupado por subgrupo."""
    hoy = datetime.now()
    ultimo_mes = hoy - timedelta(days=30)

    invoices = []
    for invoice in invoices_data:
        doc_header = invoice['Invoices']
        doc_date = datetime.strptime(doc_header['DocDate'], '%Y-%m-%d')
        if doc_date >= ultimo_mes:
            doc_lines = invoice.get('Invoices/DocumentLines', {})
            invoices.append({
                'ItemCode': doc_lines.get('ItemCode'),
                'Quantity': doc_lines.get('Quantity', 0)
            })

    return pd.DataFrame(invoices)

def combine_stock_and_sales(stock_df, invoices_df, items_data):
    """Combina DataFrames de stock y ventas, y calcula el stock en meses."""
    items_for_sales = []
    for item in items_data:
        item_code = item.get('ItemCode')
        sub_group_code = item.get('U_SC_Grupo2', None)
        sub_group_code = sub_group_code.zfill(3) if sub_group_code else None
        items_for_sales.append({
            'ItemCode': item_code,
            'SubGroupCode': sub_group_code
        })

    items_df = pd.DataFrame(items_for_sales)
    merged_sales_df = pd.merge(invoices_df, items_df, on='ItemCode', how='left')
    grouped_sales = merged_sales_df.groupby(['SubGroupCode']).agg({'Quantity': 'sum'}).reset_index()

    combined_df = pd.merge(stock_df, grouped_sales, on='SubGroupCode', how='outer')
    combined_df['Stock'] = combined_df['Stock'].fillna(0)
    combined_df['Quantity'] = combined_df['Quantity'].fillna(0)

    combined_df['StockEnMeses'] = combined_df.apply(
        lambda row: row['Stock'] / row['Quantity'] if row['Quantity'] > 0 else float('inf'),
        axis=1
    )
    combined_df['StockEnMeses'] = combined_df['StockEnMeses'].replace(float('inf'), 0)

    return combined_df

def replace_subgroup_codes_with_names(combined_df, subgroup_dict):
    """Reemplaza los códigos de subgrupo con sus nombres."""
    combined_df['SubGroup'] = combined_df['SubGroupCode'].map(subgroup_dict)
    return combined_df

def save_to_csv(dataframe, file_path):
    """Guarda un DataFrame en un archivo CSV."""
    dataframe.to_csv(file_path, index=False)

def process_data_stock_subgrupo_meses():
    """Función principal para orquestar la carga y procesamiento de datos."""
    # Cargar los datos desde archivos JSON
    items_data = load_json_data('data/items.json')
    invoices_data = load_json_data('data/Invoices.json')
    sub_grupos_data = load_json_data('data/sub_grupos_data.json')

    # Crear diccionario de subgrupos
    subgroup_dict = create_subgroup_dict(sub_grupos_data)

    # Procesar stock actual
    stock_df = process_current_stock(items_data)

    # Procesar unidades vendidas en el último mes
    invoices_df = process_sold_units(invoices_data)

    # Combinar stock y ventas
    combined_df = combine_stock_and_sales(stock_df, invoices_df, items_data)

    # Reemplazar códigos por nombres de subgrupo
    combined_df = replace_subgroup_codes_with_names(combined_df, subgroup_dict)

    # Mostrar el resultado (opcional)
    print(combined_df)

    # Guardar el resultado en un archivo CSV
    save_to_csv(combined_df, 'data_outputs/stock_y_ventas_por_subgrupo.csv')

process_data_stock_subgrupo_meses()