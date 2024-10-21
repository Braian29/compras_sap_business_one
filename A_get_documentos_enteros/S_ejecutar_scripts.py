# A_get_documentos_enteros\S_ejecutar_scripts.py
import sys, os
# Agregar el directorio raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from A_get_documentos_enteros.A_get_invoices_sell import get_creditnotes_data, get_invoice_data, get_purchaseinvoices_data, get_purchasecreditnotes_data
from A_get_documentos_enteros.A_get_item_data import get_items
from A_get_documentos_enteros.A_get_paymentterms import get_PaymentTermsTypes
from A_get_documentos_enteros.A_get_pricelists import get_PriceLists
from A_get_documentos_enteros.A_get_provider_data import get_supplier
from A_get_documentos_enteros.A_get_salespersons import get_salesperson
from A_get_documentos_enteros.A_get_sub_grupos import get_sub_grupos

from A_get_documentos_enteros.utils_get import fecha_desde, fecha_hasta, card_code

from datetime import datetime

card_code = 30000  # CardCode para probar que funcione el script

def get_current_time():
    return datetime.now()

# Funciones wrapper asíncronas para las funciones síncronas
async def async_get_items(card_code):
    return await asyncio.to_thread(get_items, card_code)

async def async_get_invoice_data(card_code):
    return await asyncio.to_thread(get_invoice_data, fecha_desde, fecha_hasta, card_code)

async def async_get_creditnotes_data(card_code):
    return await asyncio.to_thread(get_creditnotes_data, fecha_desde, fecha_hasta, card_code)

async def async_get_purchaseinvoices_data(card_code):
    return await asyncio.to_thread(get_purchaseinvoices_data, fecha_desde, fecha_hasta, card_code)

async def async_get_purchasecreditnotes_data(card_code):
    return await asyncio.to_thread(get_purchasecreditnotes_data, fecha_desde, fecha_hasta, card_code)

async def async_get_PaymentTermsTypes():
    return await asyncio.to_thread(get_PaymentTermsTypes)

async def async_get_PriceLists():
    return await asyncio.to_thread(get_PriceLists)

async def async_get_supplier(card_code):
    return await asyncio.to_thread(get_supplier, card_code)

async def async_get_salesperson():
    return await asyncio.to_thread(get_salesperson)

async def async_get_sub_grupos():
    return await asyncio.to_thread(get_sub_grupos)

# Definimos una función asíncrona para ejecutar todas las tareas
async def run_all_tasks_get_info(card_code):
    tasks = [
        async_get_items(card_code),
        async_get_invoice_data(card_code),
        async_get_creditnotes_data(card_code),
        async_get_purchaseinvoices_data(card_code),
        async_get_purchasecreditnotes_data(card_code),
        async_get_PaymentTermsTypes(),
        async_get_PriceLists(),
        async_get_supplier(card_code),
        async_get_salesperson(),
        async_get_sub_grupos()
    ]
    
    # Esperar a que todas las tareas se completen
    results = await asyncio.gather(*tasks)
    return results

# Ejecutar la función de forma asíncrona
if __name__ == "__main__":
    start_time = get_current_time()

    results = asyncio.run(run_all_tasks_get_info(card_code))  # Pasar card_code aquí

    end_time = get_current_time()
    duration = end_time - start_time
    print(f"El script tardó {duration} en ejecutarse")
