import requests
from A_get_documentos_enteros.Sesion import cookies, headers
from A_get_documentos_enteros.utils_get import base_url, card_code, save_data_to_json

def get_salesperson_data(base_url, card_code):
    url = base_url + f"SalesPersons?$select=SalesEmployeeCode, SalesEmployeeName, Telephone, Mobile, Email"
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

def get_salesperson():
    file_path = 'data/SalesPersons_data.json'
    supplier_data = get_salesperson_data(base_url, card_code)
    save_data_to_json(supplier_data, file_path)

if __name__ == "__main__":
    get_salesperson()
