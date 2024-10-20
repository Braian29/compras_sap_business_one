import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""#_Inicio de Sesión."""

url = "https://177.85.33.53:50695/b1s/v1/Login"
headers = {'Content-Type': 'application/json', 'Prefer': 'odata.maxpagesize=500000'}
data = {"CompanyDB":"SUPERCLIN", "Password":"Fran555?", "UserName":"hrodriguez"}

response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

if response.status_code == 200:
    # Inicio de sesión exitoso
    print('---Conexión Exitosa---')
    cookies = response.cookies
else:
    # Inicio de sesión fallido
    print(response.text)