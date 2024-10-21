# B_features\S_ejecutar_features.py
import sys, os
# Agregar el directorio raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from B_features.A_profit_montos_mensual import process_data_profit
from B_features.A_stock_meses_subgrupo import process_data_stock_subgrupo_meses
from B_features.A_unidades_mensual_subgrupos import process_unidades_subgrupo_meses
import asyncio
from datetime import datetime

def get_current_time():
    return datetime.now()

# Funciones wrapper asíncronas para las funciones síncronas
async def async_process_data_profit():
    return await asyncio.to_thread(process_data_profit)

async def async_process_data_stock_subgrupo_meses():
    return await asyncio.to_thread(process_data_stock_subgrupo_meses)

async def async_process_unidades_subgrupo_meses():
    return await asyncio.to_thread(process_unidades_subgrupo_meses)


# Definimos una función asíncrona para ejecutar todas las tareas
async def run_all_tasks_features():
    tasks = [
        async_process_data_profit(),
        async_process_data_stock_subgrupo_meses(),
        async_process_unidades_subgrupo_meses()
    ]
    
    # Esperar a que todas las tareas se completen
    results = await asyncio.gather(*tasks)
    return results


# Ejecutar la función de forma asíncrona
if __name__ == "__main__":
    start_time = get_current_time()

    results = asyncio.run(run_all_tasks_features())

    end_time = get_current_time()
    duration = end_time - start_time
    print(f"El script tardó {duration} en ejecutarse")
