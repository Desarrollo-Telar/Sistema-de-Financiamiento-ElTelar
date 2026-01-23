/* ===============================
   CONFIGURACIÓN GLOBAL
=================================*/
const charts = {};

// Obtener el protocolo (HTTP/HTTPS)
const protocolo = window.location.protocol; // Ejemplo: "https:"

// Obtener el dominio (hostname)
const dominio = window.location.hostname; // Ejemplo: "example.com"

// Obtener el puerto
const puerto = window.location.port; // Ejemplo: "8080" o "" si no está explícito
const baseUrl = `${protocolo}//${dominio}${puerto ? `:${puerto}` : ''}`;

const API = () => `${baseUrl}/kpi`;
console.log(API)
/* ===============================
   UTILIDADES
=================================*/
const formatCurrency = v =>
  'Q' + Number(v).toLocaleString('es-GT', { minimumFractionDigits: 2 });

const showMessage = (msg, type = 'success') => {
  const div = document.getElementById('messages');
  const el = document.createElement('div');
  el.className = type;
  el.textContent = msg;
  div.appendChild(el);
  setTimeout(() => el.remove(), 4000);
};

async function fetchData(endpoint) {
  try {
    const res = await fetch(`${API()}/${endpoint}`);
    if (!res.ok) throw new Error(res.statusText);
    return await res.json();
  } catch (e) {
    showMessage(`Error en ${endpoint}`, 'error');
    console.error(e);
    return [];
  }
}


function createChart(id, config) {
  if (charts[id]) charts[id].destroy();
  charts[id] = new Chart(document.getElementById(id), config);
}

const labels_mes = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
];
const currentYear = new Date().getFullYear();

async function clientesPorMes() {
  const data = await fetchData('clientes-por-mes/');

  const labels = data.map(i => {
    // 1. Convertimos el string de la API en un objeto Date real
    const fecha = new Date(i.mes); 
    
    // 2. Extraemos el índice del mes (0-11) y el año
    // Usamos getUTCMonth para evitar problemas de zona horaria si la API manda 00:00:00
    const indiceMes = fecha.getUTCMonth(); 
    const anio = fecha.getUTCFullYear();

    // 3. Obtenemos el nombre del mes desde tu array global 'labels_mes'
    const nombreMes = labels_mes[indiceMes];

    return `${nombreMes} ${anio}`;
  });

  const values = data.map(i => i.total);

  createChart('clientesMesChart', {
    type: 'line',
    data: { 
      labels: labels, 
      datasets: [{ 
        label: 'Clientes', 
        data: values, 
        fill: true,
        borderColor: 'rgb(59, 130, 246)',
        tension: 0.3 // Esto suaviza un poco la línea como en tu imagen
      }] 
    },
    options: { 
      responsive: true, 
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: {
            maxRotation: 45, // Evita que se amontonen demasiado
            minRotation: 45
          }
        }
      }
    }
  });

  document.getElementById('totalClientes').textContent =
    values.reduce((a, b) => a + b, 0).toLocaleString();
}

async function creditosPorMes() {
  const data = await fetchData('creditos-por-mes/');
  if (!data.length) return;

  // 1. Procesar y ordenar cronológicamente
  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return {
      total: i.total,
      mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`,
      timestamp: fecha.getTime()
    };
  }).sort((a, b) => a.timestamp - b.timestamp);

  const labels = dataProcesada.map(i => i.mesFormateado);
  const values = dataProcesada.map(i => i.total);

  createChart('creditosMesChart', {
    type: 'bar',
    data: { 
      labels, 
      datasets: [{ 
        label: 'Créditos', 
        data: values,
        backgroundColor: 'rgba(59, 130, 246, 0.7)', // Azul profesional
        borderColor: '#3b82f6',
        borderWidth: 1,
        borderRadius: 4
      }] 
    },
    options: { 
      responsive: true, 
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, ticks: { precision: 0 } }
      }
    }
  });

  document.getElementById('totalCreditos').textContent =
    values.reduce((a, b) => a + b, 0).toLocaleString();
}

async function creditosPorAsesor() {
  const data = await fetchData('creditos-por-asesor-mes/');
  if (!data.length) return;

  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return {
      ...i,
      mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`,
      nombreCompleto: `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim() || 'SIN ASESOR',
      timestamp: fecha.getTime()
    };
  }).sort((a, b) => a.timestamp - b.timestamp);

  const labels = [...new Set(dataProcesada.map(i => i.mesFormateado))];
  const asesores = [...new Set(dataProcesada.map(i => i.nombreCompleto))];

  const datasets = asesores.map((asesor, idx) => ({
    label: asesor,
    data: labels.map(mesLabel => {
      const registro = dataProcesada.find(
        i => i.mesFormateado === mesLabel && i.nombreCompleto === asesor
      );
      return registro ? registro.total : 0;
    }),
    // Asignamos colores de la paleta que definimos antes
    backgroundColor: colorPalette[idx % colorPalette.length] + 'CC', // CC añade transparencia
    borderColor: colorPalette[idx % colorPalette.length],
    borderWidth: 1,
    borderRadius: 2
  }));

  createChart('clientesAsesorChart', {
    type: 'bar', 
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 12 } }
      },
      scales: {
        x: { stacked: true }, // Las barras apiladas se ven mucho mejor por asesor
        y: { stacked: true, beginAtZero: true, ticks: { precision: 0 } }
      }
    }
  });
}

// Paleta de colores reutilizable para gráficas circulares
const colorPalette = [
  '#3b82f6', // Azul
  '#10b981', // Verde
  '#f59e0b', // Naranja
  '#ef4444', // Rojo
  '#8b5cf6', // Morado
  '#06b6d4', // Cian
  '#ec4899'  // Rosa
];

async function tiposCredito() {
  const data = await fetchData('tipos-credito/');
  if (!data.length) return;

  createChart('tiposCreditoChart', {
    type: 'doughnut',
    data: {
      labels: data.map(i => i.tipo_credito),
      datasets: [{
        data: data.map(i => i.cantidad),
        backgroundColor: colorPalette,
        hoverOffset: 10, // Efecto visual al pasar el mouse
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { padding: 20, usePointStyle: true }
        }
      },
      cutout: '70%' // Hace el anillo más delgado y elegante
    }
  });
}

async function formasPago() {
  const data = await fetchData('formas-pago/');
  if (!data.length) return;

  createChart('formasPagoChart', {
    type: 'pie',
    data: {
      labels: data.map(i => i.forma_de_pago),
      datasets: [{
        data: data.map(i => i.cantidad),
        backgroundColor: colorPalette.slice().reverse(), // Invertimos colores para variar
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { padding: 20, usePointStyle: true }
        }
      }
    }
  });
}

async function desembolsos() {
  const data = await fetchData('desembolsos-por-mes/');
  if (!data.length) return;

  // 1️⃣ Procesamos los datos: Convertimos el string de fecha a "Mes Año" 
  // y ordenamos cronológicamente (ascendente)
  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return {
      total: i.total,
      mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`,
      timestamp: fecha.getTime()
    };
  }).sort((a, b) => a.timestamp - b.timestamp); // Ordenar de más antiguo a más reciente

  // 2️⃣ Extraemos labels y valores ya ordenados
  const labels = dataProcesada.map(i => i.mesFormateado);
  const values = dataProcesada.map(i => i.total);

  // 3️⃣ Creamos la gráfica
  createChart('desembolsosChart', {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{ 
        label: 'Desembolsos', 
        data: values, 
        fill: true,
        borderColor: '#10b981', // Un verde esmeralda suele ir bien con desembolsos
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.3
      }]
    },
    options: { 
      responsive: true, 
      maintainAspectRatio: false,
      plugins: {
        legend: { display: true }
      }
    }
  });

  // 4️⃣ Total acumulado formateado
  document.getElementById('totalDesembolsos').textContent =
    formatCurrency(values.reduce((a, b) => a + b, 0));
}

async function recuperacion() {
  const data = await fetchData('recuperacion-mensual/');
  if (!data.length) return;

  // 1️⃣ Procesamos los datos para tener nombres de mes y años correctos
  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return {
      ...i,
      mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`,
      timestamp: fecha.getTime()
    };
  }).sort((a, b) => a.timestamp - b.timestamp); // Ordenamos cronológicamente

  const labels = dataProcesada.map(i => i.mesFormateado);

  // 2️⃣ Creamos la gráfica con los tres datasets
  createChart('recuperacionChart', {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        { 
          label: 'Mora', 
          data: dataProcesada.map(i => i.mora),
          backgroundColor: '#ef4444' // Rojo
        },
        { 
          label: 'Interés', 
          data: dataProcesada.map(i => i.interes),
          backgroundColor: '#f59e0b' // Ámbar/Naranja
        },
        { 
          label: 'Capital', 
          data: dataProcesada.map(i => i.capital),
          backgroundColor: '#3b82f6' // Azul
        }
      ]
    },
    options: { 
      responsive: true, 
      maintainAspectRatio: false,
      scales: {
        x: {
          stacked: true, // Opcional: apila las barras para ver el total por mes
        },
        y: {
          stacked: true,
          beginAtZero: true,
          ticks: {
            callback: value => 'Q' + value.toLocaleString() // Formato moneda en el eje Y
          }
        }
      },
      plugins: {
        legend: { position: 'bottom' }
      }
    }
  });

  // 3️⃣ Cálculo del gran total formateado
  const granTotal = dataProcesada.reduce((a, b) => a + b.capital + b.interes + b.mora, 0);
  document.getElementById('totalRecuperacion').textContent = formatCurrency(granTotal);
}

async function egresos() {
  const data = await fetchData('egresos-por-codigo-mes/');
  if (!data.length) return;

  // 1. Procesar datos para limpiar fechas y asegurar el orden
  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return {
      ...i,
      mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`,
      timestamp: fecha.getTime()
    };
  }).sort((a, b) => a.timestamp - b.timestamp);

  // 2. Extraer etiquetas únicas (Meses y Códigos de Egreso)
  const labels = [...new Set(dataProcesada.map(i => i.mesFormateado))];
  const codigosUnicos = [...new Set(dataProcesada.map(i => i.codigo_egreso))];

  // 3. Crear un Dataset por cada Código de Egreso
  const datasets = codigosUnicos.map((codigo) => {
    return {
      label: codigo,
      data: labels.map(mesLabel => {
        // Buscamos el registro que coincida con el mes y el código
        const registro = dataProcesada.find(
          i => i.mesFormateado === mesLabel && i.codigo_egreso === codigo
        );
        return registro ? registro.monto : 0;
      }),
      // Generamos un color aleatorio o puedes usar una paleta fija
      backgroundColor: `hsl(${Math.random() * 360}, 70%, 60%)`,
      borderWidth: 1
    };
  });

  // 4. Configurar y crear la gráfica
  createChart('egresosChart', {
    type: 'bar',
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right', // Leyenda a la derecha para no quitar espacio
          labels: { boxWidth: 12, font: { size: 10 } }
        },
        tooltip: {
          callbacks: {
            label: (context) => `${context.dataset.label}: Q${context.raw.toLocaleString()}`
          }
        }
      },
      scales: {
        x: { 
          stacked: true, // APILADO
          ticks: { maxRotation: 45, minRotation: 45 }
        },
        y: { 
          stacked: true, // APILADO
          beginAtZero: true,
          ticks: {
            callback: value => 'Q' + value.toLocaleString()
          }
        }
      }
    }
  });
}

async function bancos() {
  const data = await fetchData('bancos-por-mes/');
  if (!data.length) return;

  // 1. Procesar y ordenar los datos cronológicamente
  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return {
      ...i,
      mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`,
      timestamp: fecha.getTime()
    };
  }).sort((a, b) => a.timestamp - b.timestamp);

  // 2. Extraer etiquetas y valores ordenados
  const labels = dataProcesada.map(i => i.mesFormateado);
  
  // Usamos los datos de dataProcesada para que coincidan con el orden de los meses
  const saldos = dataProcesada.map(i => i.saldos);
  const ingresos = dataProcesada.map(i => i.ingreso);
  const egresos = dataProcesada.map(i => i.egreso);

  // 3. Crear la gráfica
  createChart('bancosChart', {
    type: 'bar', // Gráfica de barras para comparar flujos
    data: {
      labels: labels,
      datasets: [
        { 
          label: 'Ingresos', 
          data: ingresos, 
          backgroundColor: 'rgba(16, 185, 129, 0.7)', // Verde
          borderColor: '#10b981',
          borderWidth: 1
        },
        { 
          label: 'Egresos', 
          data: egresos, 
          backgroundColor: 'rgba(239, 68, 68, 0.7)', // Rojo
          borderColor: '#ef4444',
          borderWidth: 1
        },
        { 
          label: 'Saldos', 
          type: 'line', // Convertimos saldos a línea para destacar la tendencia
          data: saldos, 
          borderColor: '#3b82f6', // Azul
          backgroundColor: 'transparent',
          tension: 0.3,
          fill: false,
          pointStyle: 'circle',
          pointRadius: 5
        }
      ]
    },
    options: { 
      responsive: true, 
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom' },
        tooltip: {
          callbacks: {
            label: (context) => `${context.dataset.label}: Q${context.raw.toLocaleString()}`
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: value => 'Q' + value.toLocaleString()
          }
        }
      }
    }
  });

  // 4. Mostrar el saldo total más reciente (último mes del array ordenado)
  const ultimoSaldo = saldos[saldos.length - 1] || 0;
  document.getElementById('totalBancos').textContent = formatCurrency(ultimoSaldo);
}

async function acreedores() {
  const data = await fetchData('acreedores-por-mes/');
  if (!data.length) return;

  // 1. Procesar y ordenar los datos (Importante para que coincidan con los labels)
  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return {
      ...i,
      mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`,
      timestamp: fecha.getTime()
    };
  }).sort((a, b) => a.timestamp - b.timestamp);

  // 2. Extraer los labels ordenados
  const labels = dataProcesada.map(i => i.mesFormateado);

  // 3. Crear la gráfica
  createChart('acreedoresChart', {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        { 
          label: 'Pagos', 
          data: dataProcesada.map(i => i.pagos), 
          borderColor: '#3b82f6', // Azul
          backgroundColor: 'transparent',
          tension: 0.3
        },
        { 
          label: 'Mora Pagada', 
          data: dataProcesada.map(i => i.mora_pagada), 
          borderColor: '#ef4444', // Rojo
          backgroundColor: 'transparent',
          tension: 0.3
        },
        { 
          label: 'Interés Pagado', 
          data: dataProcesada.map(i => i.interes_pagado), 
          borderColor: '#f59e0b', // Naranja
          backgroundColor: 'transparent',
          tension: 0.3
        },
        { 
          label: 'Aportes A Capital', 
          data: dataProcesada.map(i => i.aporte_capital), 
          borderColor: '#10b981', // Verde
          backgroundColor: 'transparent',
          tension: 0.3
        }
      ]
    },
    options: { 
      responsive: true, 
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom' },
        tooltip: {
          mode: 'index',
          intersect: false, // Permite ver todos los valores al pasar el mouse cerca
          callbacks: {
            label: (context) => `${context.dataset.label}: Q${context.raw.toLocaleString()}`
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: value => 'Q' + value.toLocaleString()
          }
        }
      }
    }
  });
}

async function morosidad() {
  const data = await fetchData('morosidad-por-mes/');
  if (!data.length) return;

  // 1. Procesamos y ordenamos los datos
  const dataProcesada = data.map(i => {
    const fecha = new Date(i.periodo);
    return {
      cantidad: i.cantidad,
      mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`,
      timestamp: fecha.getTime()
    };
  }).sort((a, b) => a.timestamp - b.timestamp); // Orden ascendente

  // 2. Extraemos labels y valores de los datos ya procesados
  const labels = dataProcesada.map(i => i.mesFormateado);
  const values = dataProcesada.map(i => i.cantidad);

  // 3. Creamos la gráfica
  createChart('morosidadChart', {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{ 
        label: 'Clientes en Mora', 
        data: values, 
        fill: true,
        borderColor: '#f43f5e', // Color rosado/rojo para alerta de mora
        backgroundColor: 'rgba(244, 63, 94, 0.1)',
        tension: 0.3 
      }]
    },
    options: { 
      responsive: true, 
      maintainAspectRatio: false,
      plugins: {
        legend: { display: true }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { precision: 0 } // Para que no muestre decimales en cantidad de clientes
        }
      }
    }
  });

  // 4. Actualizamos el indicador numérico
  document.getElementById('totalMorosidad').textContent =
    values.reduce((a, b) => a + b, 0).toLocaleString();
}

async function casos_exito_asesor() {
  const data = await fetchData('casos-exito-asesor/');
  if (!data.length) return;

  // 1. Extraemos los nombres
  const labels = data.map(i =>
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim()
  );

  // 2. Extraemos los dos nuevos valores de la API
  const otorgados = data.map(i => i.total_otorgados);
  const cancelados = data.map(i => i.total_cancelados);

  createChart('casosExitoChart', {
    type: 'bar',
    data: { 
      labels, 
      datasets: [
        { 
          label: 'Total Otorgados', 
          data: otorgados,
          backgroundColor: 'rgba(54, 162, 235, 0.5)', // Azul transparente
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          borderRadius: 5
        },
        { 
          label: 'Cancelados (Éxito)', 
          data: cancelados,
          backgroundColor: 'rgba(75, 192, 192, 0.8)', // Esmeralda sólido
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          borderRadius: 5
        }
      ] 
    },
    options: { 
      indexAxis: 'y', 
      responsive: true, 
      maintainAspectRatio: false,
      plugins: {
        legend: { 
          display: true, 
          position: 'top' // Mostramos leyenda para distinguir las barras
        },
        tooltip: {
          callbacks: {
            // Agregamos el porcentaje de éxito al pasar el mouse
            afterLabel: function(context) {
              const index = context.dataIndex;
              const porcentaje = ((cancelados[index] / otorgados[index]) * 100).toFixed(1);
              return `Efectividad: ${porcentaje}%`;
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          title: { display: true, text: 'Cantidad de Créditos' }
        }
      }
    }
  });
}

async function casos_judicial_asesor() {
  const data = await fetchData('casos-demanda-asesor/');
  if (!data.length) return;

  // 1. Extraemos los nombres
  const labels = data.map(i =>
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim()
  );

  // 2. Extraemos los dos nuevos valores de la API
  const otorgados = data.map(i => i.total_otorgados);
  const cancelados = data.map(i => i.total_demandados);

  createChart('casosDemandaChart', {
    type: 'bar',
    data: { 
      labels, 
      datasets: [
        { 
          label: 'Total Otorgados', 
          data: otorgados,
          backgroundColor: 'rgba(54, 162, 235, 0.5)', // Azul transparente
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          borderRadius: 5
        },
        { 
          label: 'Demandados', 
          data: cancelados,
          backgroundColor: 'rgba(75, 192, 192, 0.8)', // Esmeralda sólido
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          borderRadius: 5
        }
      ] 
    },
    options: { 
      indexAxis: 'y', 
      responsive: true, 
      maintainAspectRatio: false,
      plugins: {
        legend: { 
          display: true, 
          position: 'top' // Mostramos leyenda para distinguir las barras
        },
        tooltip: {
          callbacks: {
            // Agregamos el porcentaje de éxito al pasar el mouse
            afterLabel: function(context) {
              const index = context.dataIndex;
              const porcentaje = ((cancelados[index] / otorgados[index]) * 100).toFixed(1);
              return `Tasa: ${porcentaje}%`;
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          title: { display: true, text: 'Cantidad de Créditos' }
        }
      }
    }
  });
}

async function casos_atraso_asesor() {
  const data = await fetchData('casos-atraso-asesor/');
  if (!data.length) return;

  // 1. Extraemos los nombres
  const labels = data.map(i =>
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim()
  );

  // 2. Extraemos los dos nuevos valores de la API
  const otorgados = data.map(i => i.total_otorgados);
  const cancelados = data.map(i => i.total_atrasados);

  createChart('casosAtrasadoChart', {
    type: 'bar',
    data: { 
      labels, 
      datasets: [
        { 
          label: 'Total Otorgados', 
          data: otorgados,
          backgroundColor: 'rgba(54, 162, 235, 0.5)', // Azul transparente
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          borderRadius: 5
        },
        { 
          label: 'Atrasados', 
          data: cancelados,
          backgroundColor: 'rgba(75, 192, 192, 0.8)', // Esmeralda sólido
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          borderRadius: 5
        }
      ] 
    },
    options: { 
      indexAxis: 'y', 
      responsive: true, 
      maintainAspectRatio: false,
      plugins: {
        legend: { 
          display: true, 
          position: 'top' // Mostramos leyenda para distinguir las barras
        },
        tooltip: {
          callbacks: {
            // Agregamos el porcentaje de éxito al pasar el mouse
            afterLabel: function(context) {
              const index = context.dataIndex;
              const porcentaje = ((cancelados[index] / otorgados[index]) * 100).toFixed(1);
              return `Tasa: ${porcentaje}%`;
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          title: { display: true, text: 'Cantidad de Créditos' }
        }
      }
    }
  });
}

async function loadAllData() {
  showMessage('Cargando KPIs...');
  await Promise.all([
    clientesPorMes(),
    creditosPorMes(),
    creditosPorAsesor(),
    tiposCredito(),
    formasPago(),
    desembolsos(),
    recuperacion(),
    egresos(),
    bancos(),
    acreedores(),
    morosidad(),
    casos_exito_asesor(),
    casos_judicial_asesor(),
    casos_atraso_asesor(),
  ]);
  showMessage('Dashboard actualizado ✅');
}

window.onload = loadAllData;