"""import json
import pandas as pd
from datetime import datetime, timedelta

# Cargar los datos desde el archivo items.json
with open('data/items.json', 'r', encoding='utf-8') as file:
    items_data = json.load(file)

# Cargar los datos desde el archivo Invoices.json
with open('data/Invoices.json', 'r', encoding='utf-8') as file:
    invoices_data = json.load(file)

# Cargar los datos desde el archivo sub_grupos_data.json
with open('data/sub_grupos_data.json', 'r', encoding='utf-8') as file:
    sub_grupos_data = json.load(file)

# Crear un diccionario para mapear los códigos a nombres
subgrupo_dict = {subgrupo['Code']: subgrupo['Name'] for subgrupo in sub_grupos_data}

# ----------- PROCESAR STOCK ACTUAL ----------- 
items = []
for item in items_data:
    sub_group_code = item.get('U_SC_Grupo2', None)
    # Asegurarse de que el código tenga 3 caracteres
    sub_group_code = sub_group_code.zfill(3) if sub_group_code else None
    # Recorrer los almacenes de cada artículo
    for warehouse in item.get('ItemWarehouseInfoCollection', []):
        stock = warehouse.get('InStock', 0)
        # Agregar una entrada por cada combinación de subgrupo y stock
        items.append({
            'SubGroupCode': sub_group_code,
            'Stock': stock
        })

# Crear DataFrame para stock actual
stock_df = pd.DataFrame(items)

# Agrupar solo por código de subgrupo, sumando el stock total
grouped_stock = stock_df.groupby(['SubGroupCode']).agg({'Stock': 'sum'}).reset_index()

# ----------- PROCESAR UNIDADES VENDIDAS (ÚLTIMO MES) ----------- 
# Calcular la fecha límite del último mes
hoy = datetime.now()
ultimo_mes = hoy - timedelta(days=30)

invoices = []
for invoice in invoices_data:
    doc_header = invoice['Invoices']
    doc_date = datetime.strptime(doc_header['DocDate'], '%Y-%m-%d')
    
    # Filtrar las facturas del último mes
    if doc_date >= ultimo_mes:
        doc_lines = invoice.get('Invoices/DocumentLines', {})
        invoices.append({
            'ItemCode': doc_lines.get('ItemCode'),
            'Quantity': doc_lines.get('Quantity', 0)  # Unidades vendidas
        })

invoices_df = pd.DataFrame(invoices)

# Relacionar ItemCode en facturas con los subgrupos de items.json
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

# Combinar los datos de facturas con los subgrupos correspondientes
merged_sales_df = pd.merge(invoices_df, items_df, on='ItemCode', how='left')

# Agrupar solo por código de subgrupo, sumando las unidades vendidas
grouped_sales = merged_sales_df.groupby(['SubGroupCode']).agg({'Quantity': 'sum'}).reset_index()

# ----------- COMBINAR STOCK Y VENTAS ----------- 
# Unir ambos DataFrames (stock y ventas) en uno solo
combined_df = pd.merge(grouped_stock, grouped_sales, on='SubGroupCode', how='outer')

# Rellenar valores nulos con 0 (en caso de que no haya ventas o stock en algún subgrupo)
combined_df['Stock'] = combined_df['Stock'].fillna(0)
combined_df['Quantity'] = combined_df['Quantity'].fillna(0)

# ----------- CALCULAR STOCK EN MESES ----------- 
# Evitar división por cero
combined_df['StockEnMeses'] = combined_df.apply(
    lambda row: row['Stock'] / row['Quantity'] if row['Quantity'] > 0 else float('inf'),
    axis=1
)

# Convertir valores infinitos a 0
combined_df['StockEnMeses'] = combined_df['StockEnMeses'].replace(float('inf'), 0)

# ----------- REEMPLAZAR CÓDIGOS POR NOMBRES DE SUBGRUPO ----------- 
combined_df['SubGroup'] = combined_df['SubGroupCode'].map(subgrupo_dict)

# Mostrar el resultado
print(combined_df)

# Guardar el resultado en un archivo CSV
combined_df.to_csv('data_outputs/stock_y_ventas_por_subgrupo.csv', index=False)
"""

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