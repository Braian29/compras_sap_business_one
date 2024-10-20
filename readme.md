# Plataforma de Integración para Compras en SAP Business One

Este proyecto es una plataforma web diseñada para integrarse con la API de SAP Business One, con el fin de gestionar datos relacionados con el área de compras. El sistema permite descargar, procesar y mostrar información clave de SAP Business One, brindando funcionalidades útiles para la toma de decisiones en el área de compras.

## Tabla de Contenidos
1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Características](#características)
3. [Estructura de Carpetas](#estructura-de-carpetas)
4. [Instalación](#instalación)
5. [Uso](#uso)
6. [Endpoints de la API](#endpoints-de-la-api)
7. [Integración Frontend](#integración-frontend)
8. [Tareas Pendientes / Futuras Mejoras](#tareas-pendientes--futuras-mejoras)

---

## Descripción del Proyecto

La plataforma se conecta con SAP Business One para descargar documentos de compras y otros datos relevantes mediante la API de SAP B1. Estos datos se procesan y transforman en métricas y resúmenes útiles, los cuales son visualizados en el frontend.

### Flujo de Trabajo:
1. **Descarga de datos**: Se obtienen documentos completos de la API de SAP Business One (`get_documentos_enteros`).
2. **Obtención de features**: Se generan y calculan características relevantes a partir de los datos descargados.
3. **Carga de datos**: Se cargan los datos procesados en la API de la aplicación.
4. **Visualización**: Los datos se muestran en la interfaz web del usuario.

---

## Características

- **Integración con SAP Business One**: Descarga de facturas y notas de crédito de ventas y de compras, listas de precios, información de proveedores, de vendedores, de sub grupos.
- **Procesamiento de datos**: Obtención de características y cálculos, como el stock por subgrupos y el total de unidades y ventas mensuales.
- **API REST**: Exposición de los datos procesados a través de una API.
- **Frontend dinámico**: Visualización de informes y resúmenes en el dashboard de la aplicación.

---

## Estructura de Carpetas

La estructura del proyecto es la siguiente:

```bash
.
├── __pycache__
├── 1_get_documentos_enteros
│   ├── __pycache__
│   ├── A_get_invoices_sell.py
│   ├── A_get_item_data.py
│   ├── A_get_paymentterms.py
│   ├── A_get_pricelists.py
│   ├── A_get_provider_data.py
│   ├── A_get_salespersons.py
│   ├── A_get_sub_grupos.py
│   ├── S_ejecutar_scripts.py
│   ├── Sesion.py
│   └── utils_get.py
├── 2_features
│   ├── stock_subgrupo.py
│   └── unidades_y_totales_mensual.py
├── app
│   ├── __pycache__
│   ├── api
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   ├── credit_notes.py
│   │   ├── invoices.py
│   │   ├── profit.py
│   │   ├── purchase_credit_notes.py
│   │   ├── purchase_invoices.py
│   │   ├── stock_subgrupos.py
│   │   ├── supplier.py
│   │   └── utils.py
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   ├── js
│   │   │   └── script.js
│   ├── templates
│   │   └── dashboard.html
│   ├── __init__.py
│   └── app.py
├── data
│   ├── CreditNotes.json
│   ├── Invoices.json
│   ├── items.json
│   ├── PaymentTermsTypes_data.json
│   ├── PriceLists_data.json
│   ├── PurchaseCreditNotes.json
│   ├── PurchaseInvoices.json
│   ├── sub_grupos_data.json
│   └── supplier_data.json
├── data_outputs
│   ├── credit_notes_summary.csv
│   ├── invoices_summary.csv
│   ├── profit_by_month.csv
│   ├── purchase_credit_notes_summary.csv
│   ├── purchase_invoices_summary.csv
│   └── stock_y_ventas_por_subgrupo.csv
├── venv
├── ideas.md
└── readme.md
```

## Endpoints de la API

- `/api/invoices`: Obtiene un resumen de las facturas.
- `/api/credit_notes`: Muestra las notas de crédito.
- `/api/stock_subgrupos`: Presenta el stock y ventas por subgrupo.
- _(Agregar más endpoints conforme se vayan desarrollando)_

## Integración Frontend

El frontend está compuesto por un **dashboard** que permite visualizar los datos procesados. Los estilos se encuentran en `app/static/css/styles.css` y la lógica de interacción en `app/static/js/script.js`.

## Tareas Pendientes / Futuras Mejoras

- [ ] Agregar autenticación y manejo de sesiones.
- [ ] Descargar información de Ordenes de Compra y de Ingresos de Mercadería.
- [ ] Mejorar los informes del dashboard.
- [ ] Integrar gráficos visuales para resúmenes mensuales.
- [ ] Optimizar la carga y actualización de datos.
- [ ] Implementar más endpoints en la API.
