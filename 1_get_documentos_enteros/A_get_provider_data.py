import requests
from Sesion import cookies, headers
from utils_get import base_url, card_code, save_data_to_json

def get_supplier_data(base_url, card_code):
    url = base_url + f"BusinessPartners?$select=CardCode, CardName, Address, ZipCode, MailAddress, Phone1, Phone2, ContactPerson, PayTermsGrpCode, PriceListNum, FederalTaxID, FreeText, SalesPersonCode, CurrentAccountBalance, Valid, UpdateDate, CreateDate, U_U_SC_Frecuencia, U_U_SC_Secuencia, U_U_SC_Atencion &$filter=CardCode eq '{card_code}'"
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

def get_supplier():
    file_path = 'data/supplier_data.json'
    supplier_data = get_supplier_data(base_url, card_code)
    save_data_to_json(supplier_data, file_path)

if __name__ == "__main__":
    get_supplier()
