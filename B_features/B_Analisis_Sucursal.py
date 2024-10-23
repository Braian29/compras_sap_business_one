import json
import pandas as pd

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='iso-8859-1') as file:
            return json.load(file)

# Cargar los datos desde archivos JSON
items = load_json('data/items.json')
# Convertir los datos a DataFrames
df_items = pd.DataFrame(items)


# Visualizar las primeras filas de cada DataFrame
print("Items DataFrame:")
print(df_items.head())
print(df_items.columns)



"""


invoices = load_json('data/Invoices.json')
credit_notes = load_json('data/CreditNotes.json')
salesperson_data = load_json('data/SalesPersons_data.json')

df_invoices = pd.DataFrame(invoices)
df_credit_notes = pd.DataFrame(credit_notes)
df_salesperson_data = pd.DataFrame(salesperson_data)

print("Invoices DataFrame:")
print(df_invoices.head())
print(df_invoices.columns)

print("Credit Notes DataFrame:")
print(df_credit_notes.head())
print(df_credit_notes.columns)

print("Salesperson DataFrame:")
print(df_salesperson_data.head())
print(df_salesperson_data.columns)"""