/* ===============================
   CONFIGURACIÓN GLOBAL
=================================*/
const charts = {};

// Obtener el protocolo (HTTP/HTTPS)
const protocolo = window.location.protocol; 

// Obtener el dominio (hostname)
const dominio = window.location.hostname; 

// Obtener el puerto
const puerto = window.location.port; 
const baseUrl = `${protocolo}//${dominio}${puerto ? `:${puerto}` : ''}`;

// Función auxiliar para renderizar datos en las tablas del PDF/HTML
function renderTableData(tableId, rows) {
  const tableEl = document.getElementById(tableId);
  if (!tableEl) return;
  const tbody = tableEl.querySelector('tbody');
  if (!tbody) return;

  tbody.innerHTML = rows.map(cols => `
    <tr>
      ${cols.map((col, idx) => `<td class="${idx > 0 && typeof col === 'number' ? 'text-right' : ''}">${col}</td>`).join('')}
    </tr>
  `).join('');
}

const API = () => `${baseUrl}/kpi`;
console.log(API);

/* ===============================
   UTILIDADES
=================================*/
const formatCurrency = v =>
  'Q' + Number(v).toLocaleString('es-GT', { minimumFractionDigits: 2 });

const showMessage = (msg, type = 'success') => {
  const div = document.getElementById('messages');
  if (!div) return;
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

// Paleta de colores reutilizable
const colorPalette = [
  '#3b82f6', // Azul
  '#10b981', // Verde
  '#f59e0b', // Naranja
  '#ef4444', // Rojo
  '#8b5cf6', // Morado
  '#06b6d4', // Cian
  '#ec4899'  // Rosa
];

/* ===============================
   REPORTES Y GRÁFICAS
=================================*/

async function clientesPorMes() {
  const data = await fetchData('clientes-por-mes/');
  if (!data.length) return;

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

  createChart('clientesMesChart', {
    type: 'line',
    data: { 
      labels: labels, 
      datasets: [{ 
        label: 'Clientes', 
        data: values, 
        fill: true,
        borderColor: 'rgb(59, 130, 246)',
        tension: 0.3
      }] 
    },
    options: { 
      responsive: true, 
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: { maxRotation: 45, minRotation: 45 }
        }
      }
    }
  });

 
    
  // Corrección: Mapeo correcto fila por fila (Mes, Cantidad)
  renderTableData('tablaClientesMes', dataProcesada.map(i => [i.mesFormateado, i.total.toLocaleString()]));
}

async function creditosPorMes() {
  const data = await fetchData('creditos-por-mes/');
  if (!data.length) return;

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
        backgroundColor: 'rgba(59, 130, 246, 0.7)',
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

  

  // Corrección: Mapeo correcto fila por fila
  renderTableData('tablaCreditosMes', dataProcesada.map(i => [i.mesFormateado, i.total.toLocaleString()]));
}

async function creditosPorAsesor() {
  const data = await fetchData('creditos-por-asesor-mes/pdf/');
 
  if (!data || !data.length) return;

  const mesesFallback = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

  const lookupMap = new Map();
  const mesesSet = new Set();
  const asesoresSet = new Set();

  const dataProcesada = data.map(item => {
    // Parseo seguro de la fecha
    const fecha = new Date(item.mes);
    const mesIdx = isNaN(fecha.getTime()) ? 0 : fecha.getMonth();
    const anio = isNaN(fecha.getTime()) ? '' : fecha.getFullYear();
    
    const nombreMes = (typeof labels_mes !== 'undefined' && labels_mes[mesIdx]) 
      ? labels_mes[mesIdx] 
      : mesesFallback[mesIdx];
      
    const mesLabel = `${nombreMes} ${anio}`.trim();

    // Soporte tanto para 'item.asesor' como para los campos de Django por separado
    const nombreRaw = item.asesor || `${item.asesor_de_credito__nombre || ''} ${item.asesor_de_credito__apellido || ''}`;
    const asesorNombre = nombreRaw.trim() || 'SIN ASESOR';

    mesesSet.add(mesLabel);
    asesoresSet.add(asesorNombre);

    lookupMap.set(`${mesLabel}_${asesorNombre}`, item.total);

    return {
      mesFormateado: mesLabel,
      nombreCompleto: asesorNombre,
      total: item.total
    };
  });

  const labels = Array.from(mesesSet);
  const asesores = Array.from(asesoresSet);

  const datasets = asesores.map((asesor, idx) => {
    const color = (typeof colorPalette !== 'undefined' && colorPalette[idx % colorPalette.length]) 
      ? colorPalette[idx % colorPalette.length] 
      : '#3b82f6';

    return {
      label: asesor,
      data: labels.map(mesLabel => lookupMap.get(`${mesLabel}_${asesor}`) || 0),
      backgroundColor: color + 'CC',
      borderColor: color,
      borderWidth: 1,
      borderRadius: 2
    };
  });

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
        x: { stacked: true },
        y: { stacked: true, beginAtZero: true, ticks: { precision: 0 } }
      }
    }
  });

  renderTableData('tablaClientesAsesor', dataProcesada.map(i => [
    i.mesFormateado,
    i.nombreCompleto,
    i.total
  ]));
}

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
        hoverOffset: 10,
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
      cutout: '70%'
    }
  });
  renderTableData('tablaTiposCredito', data.map(i => [i.tipo_credito, i.cantidad]));
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
        backgroundColor: colorPalette.slice().reverse(),
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
  renderTableData('tablaFormasPago', data.map(i => [i.forma_de_pago, i.cantidad]));
}

async function desembolsos() {
  const data = await fetchData('desembolsos-por-mes/');
  if (!data.length) return;

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

  createChart('desembolsosChart', {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{ 
        label: 'Desembolsos', 
        data: values, 
        fill: true,
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.3
      }]
    },
    options: { 
      responsive: true, 
      maintainAspectRatio: false,
      plugins: { legend: { display: true } }
    }
  });

 

  // Corrección: Se agregó renderTableData que faltaba
  renderTableData('tablaDesembolsos', dataProcesada.map(i => [i.mesFormateado, formatCurrency(i.total)]));
}

async function recuperacion() {
  const data = await fetchData('recuperacion-mensual/');
  if (!data.length) return;

  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return {
      ...i,
      mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`,
      timestamp: fecha.getTime()
    };
  }).sort((a, b) => a.timestamp - b.timestamp);

  const labels = dataProcesada.map(i => i.mesFormateado);

  createChart('recuperacionChart', {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        { 
          label: 'Mora', 
          data: dataProcesada.map(i => i.mora),
          backgroundColor: '#ef4444'
        },
        { 
          label: 'Interés', 
          data: dataProcesada.map(i => i.interes),
          backgroundColor: '#f59e0b'
        },
        { 
          label: 'Capital', 
          data: dataProcesada.map(i => i.capital),
          backgroundColor: '#3b82f6'
        }
      ]
    },
    options: { 
      responsive: true, 
      maintainAspectRatio: false,
      scales: {
        x: { stacked: true },
        y: {
          stacked: true,
          beginAtZero: true,
          ticks: {
            callback: value => 'Q' + value.toLocaleString()
          }
        }
      },
      plugins: { legend: { position: 'bottom' } }
    }
  });

  const granTotal = dataProcesada.reduce((a, b) => a + b.capital + b.interes + b.mora, 0);
  

  renderTableData('tablaRecuperacion', dataProcesada.map(i => [
    i.mesFormateado, 
    formatCurrency(i.capital), 
    formatCurrency(i.interes), 
    formatCurrency(i.mora)
  ]));
}

async function egresos() {
  const data = await fetchData('egresos-por-codigo-mes/');
  if (!data.length) return;

  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return {
      ...i,
      mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`,
      timestamp: fecha.getTime()
    };
  }).sort((a, b) => a.timestamp - b.timestamp);

  const labels = [...new Set(dataProcesada.map(i => i.mesFormateado))];
  const codigosUnicos = [...new Set(dataProcesada.map(i => i.codigo_egreso))];

  const datasets = codigosUnicos.map((codigo) => {
    return {
      label: codigo,
      data: labels.map(mesLabel => {
        const registro = dataProcesada.find(
          i => i.mesFormateado === mesLabel && i.codigo_egreso === codigo
        );
        return registro ? registro.monto : 0;
      }),
      backgroundColor: `hsl(${Math.random() * 360}, 70%, 60%)`,
      borderWidth: 1
    };
  });

  createChart('egresosChart', {
    type: 'bar',
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
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
          stacked: true,
          ticks: { maxRotation: 45, minRotation: 45 }
        },
        y: { 
          stacked: true,
          beginAtZero: true,
          ticks: {
            callback: value => 'Q' + value.toLocaleString()
          }
        }
      }
    }
  });

  // Corrección: Renderizado de la tabla de egresos por código y mes
  renderTableData('tablaEgresos', dataProcesada.map(i => [
    i.mesFormateado,
    i.codigo_egreso,
    formatCurrency(i.monto)
  ]));
}

async function bancos() {
  const data = await fetchData('bancos-por-mes/');
  if (!data.length) return;

  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return {
      ...i,
      mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`,
      timestamp: fecha.getTime()
    };
  }).sort((a, b) => a.timestamp - b.timestamp);

  const labels = dataProcesada.map(i => i.mesFormateado);
  const saldos = dataProcesada.map(i => i.saldos);
  const ingresos = dataProcesada.map(i => i.ingreso);
  const egresos = dataProcesada.map(i => i.egreso);

  createChart('bancosChart', {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        { 
          label: 'Ingresos', 
          data: ingresos, 
          backgroundColor: 'rgba(16, 185, 129, 0.7)',
          borderColor: '#10b981',
          borderWidth: 1
        },
        { 
          label: 'Egresos', 
          data: egresos, 
          backgroundColor: 'rgba(239, 68, 68, 0.7)',
          borderColor: '#ef4444',
          borderWidth: 1
        },
        { 
          label: 'Saldos', 
          type: 'line',
          data: saldos, 
          borderColor: '#3b82f6',
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

  const ultimoSaldo = saldos[saldos.length - 1] || 0;
  

  renderTableData('tablaBancos', dataProcesada.map(i => [
    i.mesFormateado, 
    formatCurrency(i.ingreso), 
    formatCurrency(i.egreso), 
    formatCurrency(i.saldos)
  ]));
}

async function acreedores() {
  const data = await fetchData('acreedores-por-mes/');
  if (!data.length) return;

  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return {
      ...i,
      mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`,
      timestamp: fecha.getTime()
    };
  }).sort((a, b) => a.timestamp - b.timestamp);

  const labels = dataProcesada.map(i => i.mesFormateado);

  createChart('acreedoresChart', {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        { 
          label: 'Pagos', 
          data: dataProcesada.map(i => i.pagos), 
          borderColor: '#3b82f6',
          backgroundColor: 'transparent',
          tension: 0.3
        },
        { 
          label: 'Mora Pagada', 
          data: dataProcesada.map(i => i.mora_pagada), 
          borderColor: '#ef4444',
          backgroundColor: 'transparent',
          tension: 0.3
        },
        { 
          label: 'Interés Pagado', 
          data: dataProcesada.map(i => i.interes_pagado), 
          borderColor: '#f59e0b',
          backgroundColor: 'transparent',
          tension: 0.3
        },
        { 
          label: 'Aportes A Capital', 
          data: dataProcesada.map(i => i.aporte_capital), 
          borderColor: '#10b981',
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
          intersect: false,
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

  renderTableData('tablaAcreedores', dataProcesada.map(i => [
    i.mesFormateado,
    formatCurrency(i.pagos),
    formatCurrency(i.mora_pagada),
    formatCurrency(i.interes_pagado),
    formatCurrency(i.aporte_capital)
  ]));
}

async function morosidad() {
  const data = await fetchData('morosidad-por-mes/');
  if (!data.length) return;

  const dataProcesada = data.map(i => {
    const fecha = new Date(i.periodo);
    return {
      cantidad: i.cantidad,
      mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`,
      timestamp: fecha.getTime()
    };
  }).sort((a, b) => a.timestamp - b.timestamp);

  const labels = dataProcesada.map(i => i.mesFormateado);
  const values = dataProcesada.map(i => i.cantidad);

  createChart('morosidadChart', {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{ 
        label: 'Clientes en Mora', 
        data: values, 
        fill: true,
        borderColor: '#f43f5e',
        backgroundColor: 'rgba(244, 63, 94, 0.1)',
        tension: 0.3 
      }]
    },
    options: { 
      responsive: true, 
      maintainAspectRatio: false,
      plugins: { legend: { display: true } },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { precision: 0 }
        }
      }
    }
  });

  

  renderTableData('tablaMorosidad', dataProcesada.map(i => [i.mesFormateado, i.cantidad]));
}

async function casos_exito_asesor() {
  const data = await fetchData('casos-exito-asesor/');
  if (!data.length) return;

  const labels = data.map(i =>
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim()
  );

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
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          borderRadius: 5
        },
        { 
          label: 'Cancelados (Éxito)', 
          data: cancelados,
          backgroundColor: 'rgba(75, 192, 192, 0.8)',
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
        legend: { display: true, position: 'top' },
        tooltip: {
          callbacks: {
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

  renderTableData('tablaCasosExito', data.map(i => [
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim(),
    i.total_otorgados,
    i.total_cancelados
  ]));
}

async function casos_judicial_asesor() {
  const data = await fetchData('casos-demanda-asesor/');
  if (!data.length) return;

  const labels = data.map(i =>
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim()
  );

  const otorgados = data.map(i => i.total_otorgados);
  const demandados = data.map(i => i.total_demandados);

  createChart('casosDemandaChart', {
    type: 'bar',
    data: { 
      labels, 
      datasets: [
        { 
          label: 'Total Otorgados', 
          data: otorgados,
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          borderRadius: 5
        },
        { 
          label: 'Demandados', 
          data: demandados,
          backgroundColor: 'rgba(239, 68, 68, 0.8)',
          borderColor: 'rgba(239, 68, 68, 1)',
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
        legend: { display: true, position: 'top' },
        tooltip: {
          callbacks: {
            afterLabel: function(context) {
              const index = context.dataIndex;
              const porcentaje = ((demandados[index] / otorgados[index]) * 100).toFixed(1);
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

  renderTableData('tablaCasosDemanda', data.map(i => [
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim(),
    i.total_otorgados,
    i.total_demandados
  ]));
}

async function casos_atraso_asesor() {
  const data = await fetchData('casos-atraso-asesor/');
  if (!data.length) return;

  const labels = data.map(i =>
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim()
  );

  const otorgados = data.map(i => i.total_otorgados);
  const atrasados = data.map(i => i.total_atrasados);

  createChart('casosAtrasadoChart', {
    type: 'bar',
    data: { 
      labels, 
      datasets: [
        { 
          label: 'Total Otorgados', 
          data: otorgados,
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          borderRadius: 5
        },
        { 
          label: 'Atrasados', 
          data: atrasados,
          backgroundColor: 'rgba(245, 158, 11, 0.8)',
          borderColor: 'rgba(245, 158, 11, 1)',
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
        legend: { display: true, position: 'top' },
        tooltip: {
          callbacks: {
            afterLabel: function(context) {
              const index = context.dataIndex;
              const porcentaje = ((atrasados[index] / otorgados[index]) * 100).toFixed(1);
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

  renderTableData('tablaCasosAtrasado', data.map(i => [
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim(),
    i.total_otorgados,
    i.total_atrasados
  ]));
}

async function cartera_asesor() {
  const data = await fetchData('cartera-asesor/');
  if (!data.length) return;

  const labels = data.map(i =>
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim()
  );

  const otorgados = data.map(i => i.saldo_cartera_total);
  const cancelados = data.map(i => i.saldo_en_atraso);

  createChart('carteraAsesorChart', {
    type: 'bar',
    data: { 
      labels, 
      datasets: [
        { 
          label: 'Vigentes', 
          data: otorgados,
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          borderRadius: 5
        },
        { 
          label: 'Atrasados', 
          data: cancelados,
          backgroundColor: 'rgba(239, 68, 68, 0.8)',
          borderColor: 'rgba(239, 68, 68, 1)',
          borderWidth: 1,
          borderRadius: 5
        }
      ] 
    },
    options: { 
      indexAxis: 'x', 
      responsive: true, 
      maintainAspectRatio: false,
      plugins: {
        legend: { display: true, position: 'top' },
        tooltip: {
          callbacks: {
            afterLabel: function(context) {
              const index = context.dataIndex;
              const porcentaje = ((cancelados[index] / otorgados[index]) * 100).toFixed(1);
              return `Tasa (Saldo Atraso / Saldo Total Otorgado): ${porcentaje}%`;
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          title: { display: true, text: 'Asesores' }
        },
        y: {
          beginAtZero: true,
          ticks: {
            callback: value => 'Q' + value.toLocaleString()
          }
        }
      }
    }
  });

  renderTableData('tablaCarteraAsesor', data.map(i => [
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim(),
    formatCurrency(i.saldo_cartera_total),
    formatCurrency(i.saldo_en_atraso)
  ]));
}

/* ===============================
   INICIALIZACIÓN
=================================*/





/* ===============================
   EXPORTACIÓN A PDF (FRONTEND)
=================================*/
function descargarPDF() {
  const elemento = document.getElementById('reporte-pdf');
  
  // Opciones de configuración para html2pdf
  const opciones = {
    margin:       [10, 10, 10, 10], // Margen en mm [arriba, izquierda, abajo, derecha]
    filename:     `dashboard_${new Date().toISOString().slice(0,10)}.pdf`,
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2, useCORS: true, logging: false }, // Scale 2 asegura nitidez en canvas
    jsPDF:        { unit: 'mm', format: 'letter', orientation: 'portrait' }
  };

  // Convertir a PDF y descargar
  html2pdf().set(opciones).from(elemento).save();
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
    cartera_asesor()
  ]);
  showMessage('Dashboard actualizado ✅');

  // Pequeña pausa (500ms) para garantizar el renderizado completo de las animaciones de Chart.js
  setTimeout(() => {
     descargarPDF();
  }, 500);
}

window.onload = loadAllData;