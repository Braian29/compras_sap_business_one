import requests
from A_get_documentos_enteros.Sesion import cookies, headers
from A_get_documentos_enteros.utils_get import base_url, card_code, save_data_to_json

def get_items_data(base_url, card_code):
    url = base_url + f"Items?$select=ItemCode,ItemName,ForeignName,BarCode,Mainsupplier,SupplierCatalogNo, User_Text,Valid,PurchaseItemsPerUnit,ArTaxCode,UpdateDate,CreateDate,U_UniRefPrecio, SalesUnitVolume,U_SC_Grupo2,U_SC_Grupo,U_Rep_UxR,ItemPrices,ItemWarehouseInfoCollection &$filter=Mainsupplier eq '{card_code}'"
    all_data = []

    while url:
        response = requests.get(url, headers=headers, cookies=cookies, verify=False) 
        if response.status_code == 200: 
            data = response.json() 
            all_data.extend(data['value']) 
            next_link = data.get('odata.nextLink') 
            url = base_url + next_link if next_link else None 
        else: 
            print(f"Error en la solicitud: {response.status_code} - {response.text}") 
            break 

    return all_data 

def filter_price_lists(data):
    for item in data:
        item['ItemPrices'] = [
            {"PriceList": price['PriceList'], "Price": price['Price']}
            for price in item.get('ItemPrices', [])
            if price['PriceList'] in {1, 22, 16, 30}
        ]
    return data

def filter_warehouse_info(data):
    for item in data:
        item['ItemWarehouseInfoCollection'] = [
            {
                "MinimalStock": warehouse.get('MinimalStock'),
                "WarehouseCode": warehouse.get('WarehouseCode'),
                "InStock": warehouse.get('InStock')
            }
            for warehouse in item.get('ItemWarehouseInfoCollection', [])
        ]
    return data

def get_items(card_code):
    file_path = 'data/items.json'
    items_data = get_items_data(base_url, card_code)
    filtered_data = filter_price_lists(items_data)
    filtered_data = filter_warehouse_info(filtered_data)
    save_data_to_json(filtered_data, file_path)

if __name__ == "__main__":
    get_items()
