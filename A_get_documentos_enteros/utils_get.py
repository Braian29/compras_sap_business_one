from datetime import datetime, timedelta
import json, os

fecha_hasta = datetime.now().strftime("%Y-%m-%d")
fecha_desde = (datetime.now() - timedelta(days=395)).strftime("%Y-%m-%d")

card_code = "30002"
base_url = "https://177.85.33.53:50695/b1s/v1/"

def save_data_to_json(data, file_path):
    if data:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Datos guardados en '{file_path}'")
    else:
        print("No se obtuvieron datos o hubo un error en la extracción.")




# Crear la carpeta 'data' si no existe
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Función para guardar los datos en formato JSON
def save_to_json(data, filename):
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Datos guardados en {file_path}")