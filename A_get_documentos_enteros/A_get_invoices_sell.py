# 1_get_documentos_enteros\A_get_invoices_sell.py
import requests
import pandas as pd
import json
from A_get_documentos_enteros.Sesion import cookies, headers
from A_get_documentos_enteros.utils_get import base_url, save_to_json


# Función genérica para obtener datos de facturas o notas de crédito
def get_data_from_api(endpoint, fecha_desde, fecha_hasta, card_code, doc_type):
    url = f"{base_url}QueryService_PostQuery"
    data = {
        "QueryPath": f"$crossjoin({doc_type},{doc_type}/DocumentLines,Items)",
        "QueryOption": f"$expand={doc_type}($select=DocEntry, NumAtCard,CardName,DocDate,FederalTaxID),"
                       f"{doc_type}/DocumentLines($select=LineNum, ItemCode,Quantity,DiscountPercent,Price,VendorNum,"
                       f"WarehouseCode,LineTotal,SalesPersonCode)&$filter={doc_type}/DocEntry eq "
                       f"{doc_type}/DocumentLines/DocEntry and {doc_type}/DocumentLines/ItemCode eq Items/ItemCode "
                       f"and Items/Mainsupplier eq '{card_code}' and {doc_type}/DocDate ge '{fecha_desde}' "
                       f"and {doc_type}/DocDate le '{fecha_hasta}'"
    }

    response = requests.post(url, headers=headers, cookies=cookies, data=json.dumps(data), verify=False)

    if response.status_code == 200:
        result = response.json().get('value', [])
        
        # Guardar los datos en formato JSON
        file_name = f"{doc_type}.json"
        save_to_json(result, file_name)
        
        df = pd.json_normalize(result)
        return df
    else:
        print(f"Error al obtener los datos de {doc_type}.")
        return pd.DataFrame()



# Obtener datos de facturas de clientes
def get_invoice_data(fecha_desde, fecha_hasta, card_code):
    return get_data_from_api("Invoices", fecha_desde, fecha_hasta, card_code, "Invoices")

# Obtener datos de notas de crédito de clientes
def get_creditnotes_data(fecha_desde, fecha_hasta, card_code):
    return get_data_from_api("CreditNotes", fecha_desde, fecha_hasta, card_code, "CreditNotes")


# Obtener datos de facturas de clientes
def get_purchaseinvoices_data(fecha_desde, fecha_hasta, card_code):
    return get_data_from_api("PurchaseInvoices", fecha_desde, fecha_hasta, card_code, "PurchaseInvoices")

# Obtener datos de notas de crédito de clientes
def get_purchasecreditnotes_data(fecha_desde, fecha_hasta, card_code):
    return get_data_from_api("PurchaseCreditNotes", fecha_desde, fecha_hasta, card_code, "PurchaseCreditNotes")
