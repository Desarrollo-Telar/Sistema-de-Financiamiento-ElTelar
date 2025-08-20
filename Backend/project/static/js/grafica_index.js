import { urls_p } from './API/urls_api.js';

const ctxCustomer = document.getElementById('myChart');
const ctxCredit = document.getElementById('myChartC');


// Función para obtener datos desde la API
async function fetchData(apiUrl, year) {
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error('Error al obtener los datos');

        const apiData = await response.json();

        // Preprocesar los datos para obtener la cantidad de registros por mes para un año específico
        const monthlyData = Array(12).fill(0); // Inicializar un array con 12 elementos en 0 (uno por mes)

        apiData.forEach(item => {
            const creationDate = new Date(item.creation_date); // Convertir la fecha de creación en un objeto Date
            const recordYear = creationDate.getFullYear(); // Obtener el año de la fecha
            const month = creationDate.getMonth(); // Obtener el mes (0 = Enero, 11 = Diciembre)

            // Filtrar por el año proporcionado
            if (recordYear === year) {
                monthlyData[month] += 1; // Incrementar el contador del mes correspondiente
            }
        });

        return monthlyData;
    } catch (error) {
        console.error('Error al obtener los datos:', error);
        return null;
    }
}


// Función para crear un gráfico
function createChart(ctx, labels, data, title) {
    const chartData = {
        labels: labels,
        datasets: [{
            label: title,
            data: data,
            fill: false,
            borderColor: 'rgb(72, 7, 9)',
            tension: 0.1 // Suaviza la línea del gráfico
        }]
    };

    const config = {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            animations: {
                tension: {
                    duration: 1000,
                    easing: 'linear',
                    from: 1,
                    to: 0,
                    loop: true
                }
            },
            scales: {
                y: {
                    min: 0,
                    ticks: {
                        stepSize: 1 // Incrementos en 1 en el eje Y
                    }
                }
            }
        }
    };

    new Chart(ctx, config);
}



// Configurar las etiquetas para los meses
const labels = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
];

// Llama a la función para obtener datos y renderizar los gráficos
const currentYear = new Date().getFullYear();

(async function renderCharts() {
    // Obtener y mostrar datos para clientes
    const customerData = await fetchData(urls_p.api_url_cliente, currentYear);
    if (customerData) {
        createChart(ctxCustomer, labels, customerData, `Registros de Clientes por Mes (${currentYear})`);
    }

    // Obtener y mostrar datos para créditos
    const creditData = await fetchData(urls_p.api_url_credit, currentYear);
    if (creditData) {
        createChart(ctxCredit, labels, creditData, `Registros de Créditos por Mes (${currentYear})`);
    }

   
})();
