// Función existente para formatear números
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}



// Función existente para crear gráficos
function createChart(ctx, data, label, color) {
    console.log('Creating chart:', label, 'with data:', data);

    // Determinar la propiedad correcta para el total
    let totalProperty = 'Total';
    if (data.length > 0) {
        if ('LineTotal' in data[0]) totalProperty = 'LineTotal';
        else if ('CreditTotal' in data[0]) totalProperty = 'CreditTotal';
        else if ('PurchaseTotal' in data[0]) totalProperty = 'PurchaseTotal';
        else if ('PurchaseCreditTotal' in data[0]) totalProperty = 'PurchaseCreditTotal';
        else if ('Profit' in data[0]) totalProperty = 'Profit';  // Agregar Profit para el gráfico de rentabilidad
    }

    console.log('Using total property:', totalProperty);

    // Calcular el promedio móvil de 3 meses
    const profits = data.map(item => parseFloat(item[totalProperty]) || 0);
    const averageData = profits.map((value, index, array) => {
        if (index < 2) return null; // No calcular promedio hasta tener 3 datos
        return (array[index] + array[index - 1] + array[index - 2]) / 3;
    });

    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.Month),
            datasets: [
                {
                    label: label,
                    data: profits,
                    backgroundColor: color[0],
                    borderColor: color[1],
                    borderWidth: 1
                },
                {
                    label: 'Promedio Móvil (3 meses)',
                    data: averageData,
                    type: 'line', // Cambia a línea
                    borderColor: 'rgba(192, 196, 88, 0.1);', // Color de la línea
                    borderWidth: 2,
                    fill: false // No llenar el área bajo la línea
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Monto Total'
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + numberWithCommas(value);
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += '$' + numberWithCommas(context.parsed.y.toFixed(2));
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });
}

// Función existente para obtener datos y crear gráficos
function fetchDataAndCreateChart(url, chartId, label, color) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(`Data received for ${chartId}:`, data);
            if (!Array.isArray(data) || data.length === 0) {
                throw new Error('Data is not in the expected format');
            }
            const ctx = document.getElementById(chartId).getContext('2d');
            createChart(ctx, data, label, color);
        })
        .catch(error => {
            console.error('Error fetching data for', chartId, ':', error);
            const errorMessage = `<p class="error-message">Error loading data for ${label}: ${error.message}</p>`;
            document.getElementById(chartId).insertAdjacentHTML('afterend', errorMessage);
        });
}

// Fetch data and create charts
fetchDataAndCreateChart('/api/invoices_summary', 'invoicesChart', 'Facturas de Ventas', ['rgba(75, 192, 192, 0.6)', 'rgba(75, 192, 192, 1)']);
fetchDataAndCreateChart('/api/credit_notes_summary', 'creditNotesChart', 'Notas de Crédito de Ventas', ['rgba(255, 99, 132, 0.6)', 'rgba(255, 99, 132, 1)']);
fetchDataAndCreateChart('/api/purchase_invoices_summary', 'purchaseInvoicesChart', 'Facturas de Compras', ['rgba(54, 162, 235, 0.6)', 'rgba(54, 162, 235, 1)']);
fetchDataAndCreateChart('/api/purchase_credit_notes_summary', 'purchaseCreditNotesChart', 'Notas de Crédito de Compras', ['rgba(255, 206, 86, 0.6)', 'rgba(255, 206, 86, 1)']);

// Nuevo gráfico para Rentabilidad Mensual
fetchDataAndCreateChart('/api/profit_by_month', 'profitChart', 'Rentabilidad Mensual', ['rgba(153, 102, 255, 0.6)', 'rgba(153, 102, 255, 1)']);



// ------- STOCK DE SUCURSALES ------- //

function aplicarEstilosStockEnMeses() {
    const filas = document.querySelectorAll('#stockTable tbody tr');

    filas.forEach(fila => {
        const stockEnMesesCell = fila.cells[3]; // Columna "Stock en Meses"
        const valorStockEnMeses = stockEnMesesCell.textContent.trim();

        if (valorStockEnMeses !== 'N/A' && !isNaN(valorStockEnMeses)) {
            const numValue = parseFloat(valorStockEnMeses);
            
            if (numValue === 0) {
                stockEnMesesCell.classList.add('stock-bajo');
            } else if (numValue > 0 && numValue < 1) {
                stockEnMesesCell.classList.add('stock-medio-bajo');
            } else if (numValue >= 1 && numValue <= 3) {
                stockEnMesesCell.classList.add('stock-medio-bajo');
            } else if (numValue > 3 && numValue <= 6) {
                stockEnMesesCell.classList.add('stock-medio');
            } else if (numValue > 6) {
                stockEnMesesCell.classList.add('stock-alto');
            }
        } else {
            stockEnMesesCell.classList.add('stock-bajo');
        }
    });
}

// Función para cargar y mostrar la información de stocks en sucursales
function fetchStockData() {
    fetch('/api/stock_subgrupos') // Asegúrate de que esta URL sea correcta
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Stock data received:', data);
            if (data.length === 0) {
                throw new Error('No stock data available');
            }

            // Seleccionar el elemento donde se mostrará la tabla
            const stocksTableBody = document.getElementById('stockTable').getElementsByTagName('tbody')[0];
            stocksTableBody.innerHTML = ''; // Limpiar tabla existente

            // Generar filas de la tabla
            data.forEach(stock => {
                const row = stocksTableBody.insertRow();
                row.insertCell(0).textContent = stock.SubGroup; // Subgrupo
                row.insertCell(1).textContent = stock.Stock; // Stock total

                // Verificar si Quantity tiene un valor válido antes de usarlo
                if (stock.Quantity !== null && !isNaN(stock.Quantity)) {
                    row.insertCell(2).textContent = stock.Quantity; // Cantidad vendida
                } else {
                    row.insertCell(2).textContent = 'N/A'; // Mostrar 'N/A' si no es válido
                }

                // Verificar si StockEnMeses tiene un valor válido antes de usar toFixed()
                if (stock.StockEnMeses !== null && !isNaN(stock.StockEnMeses)) {
                    row.insertCell(3).textContent = stock.StockEnMeses.toFixed(2); // Stock en Meses
                } else {
                    row.insertCell(3).textContent = 'N/A'; // Mostrar 'N/A' si no es válido
                }
            });

            // Aplicar estilos después de actualizar la tabla
            aplicarEstilosStockEnMeses();

        })
        .catch(error => {
            console.error('Error fetching stock data:', error);
            const errorMessage = `<p class="error-message">Error loading stock data: ${error.message}</p>`;
            document.getElementById('stocksTableContainer').insertAdjacentHTML('beforeend', errorMessage);
        });
}

// Llamar a la función para cargar la información de stocks
fetchStockData();


// ------- PROVEEDOR INFO ------- //  
function fetchSupplierData(url) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Supplier data received:', data);
            displaySupplierData(data[0]);  // Display the first supplier data
        })
        .catch(error => {
            console.error('Error fetching supplier data:', error);
        });
}

function displaySupplierData(supplier) {
    const supplierDetailsDiv = document.getElementById('supplierDetails');
    supplierDetailsDiv.innerHTML = `
        <p><strong>Código:</strong> ${supplier.CardCode}</p>
        <p><strong>Nombre: ${supplier.CardName}</strong></p>
        <p><strong>Teléfono 1:</strong> ${supplier.Phone1 || 'No disponible'}</p>
        <p><strong>Teléfono 2:</strong> ${supplier.Phone2 || 'No disponible'}</p>
        <p><strong>Persona de Contacto:</strong> ${supplier.ContactPerson}</p>
        <p><strong>ID Fiscal Federal:</strong> ${supplier.FederalTaxID}</p>
        <p><strong>Saldo de Cuenta Actual:</strong> $${numberWithCommas(supplier.CurrentAccountBalance.toFixed(2))}</p>
        <p><strong>Validez:</strong> ${supplier.Valid}</p>
    `;
}


// Fetch supplier data
fetchSupplierData('/api/supplier');

// ---------- UNIDADES POR MES Y POR SUBGRUPO        ----------- //
// Función para obtener los datos de la API y graficarlos
async function obtenerYGraficarDatos() {
    try {
        const response = await fetch('/api/ventas_compras_por_subgrupo');
        const data = await response.json();

        // Procesar los datos para graficar
        const meses = [];
        const unidadesCompradas = [];
        const unidadesVendidas = [];

        // Recopilar los datos por mes
        data.forEach(item => {
            // Agregar el mes a la lista si no existe
            if (!meses.includes(item.Mes)) {
                meses.push(item.Mes);
            }
            // Sumar las unidades compradas y vendidas
            const index = meses.indexOf(item.Mes);
            if (index !== -1) {
                if (!unidadesCompradas[index]) unidadesCompradas[index] = 0;
                if (!unidadesVendidas[index]) unidadesVendidas[index] = 0;

                unidadesCompradas[index] += parseFloat(item['Unidades Compradas']);
                unidadesVendidas[index] += parseFloat(item['Unidades Vendidas']);
            }
        });

        // Crear el gráfico
        const ctx = document.getElementById('ventasComprasChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line', // Tipo de gráfico: 'line', 'bar', etc.
            data: {
                labels: meses,
                datasets: [
                    {
                        label: 'Unidades Compradas',
                        data: unidadesCompradas,
                        borderColor: 'blue',
                        fill: false,
                    },
                    {
                        label: 'Unidades Vendidas',
                        data: unidadesVendidas,
                        borderColor: 'red',
                        fill: false,
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Mes'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Unidades'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error al obtener los datos:', error);
    }
}

// Llamar a la función para obtener y graficar los datos
obtenerYGraficarDatos();
