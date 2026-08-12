/* ===============================
   CONFIGURACIÓN GLOBAL
=================================*/
const charts = {}; // Declaration necesaria para evitar errores de referencia

const protocolo = window.location.protocol; 
const dominio = window.location.hostname; 
const puerto = window.location.port; 
const baseUrl = `${protocolo}//${dominio}${puerto ? `:${puerto}` : ''}`;

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

// Desactivar animaciones para renderizado instantáneo y evitar PDF en blanco
function createChart(id, config) {
  const canvas = document.getElementById(id);
  if (!canvas) return;

  if (charts[id]) {
    charts[id].destroy();
  }

  config.options = config.options || {};
  config.options.animation = false; // Desactivar animación
  config.options.responsiveAnimationDuration = 0;

  charts[id] = new Chart(canvas, config);
}

const labels_mes = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
];

const colorPalette = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899'
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

  createChart('clientesMesChart', {
    type: 'line',
    data: { 
      labels: dataProcesada.map(i => i.mesFormateado), 
      datasets: [{ label: 'Clientes', data: dataProcesada.map(i => i.total), fill: true, borderColor: 'rgb(59, 130, 246)', tension: 0.3 }] 
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

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

  createChart('creditosMesChart', {
    type: 'bar',
    data: { 
      labels: dataProcesada.map(i => i.mesFormateado), 
      datasets: [{ label: 'Créditos', data: dataProcesada.map(i => i.total), backgroundColor: 'rgba(59, 130, 246, 0.7)', borderColor: '#3b82f6', borderWidth: 1 }] 
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  renderTableData('tablaCreditosMes', dataProcesada.map(i => [i.mesFormateado, i.total.toLocaleString()]));
}

async function creditosPorAsesor() {
  const data = await fetchData('creditos-por-asesor-mes/pdf/');
  if (!data || !data.length) return;

  const lookupMap = new Map();
  const mesesSet = new Set();
  const asesoresSet = new Set();

  const dataProcesada = data.map(item => {
    const fecha = new Date(item.mes);
    const mesIdx = isNaN(fecha.getTime()) ? 0 : fecha.getMonth();
    const anio = isNaN(fecha.getTime()) ? '' : fecha.getFullYear();
    const mesLabel = `${labels_mes[mesIdx] || 'Enero'} ${anio}`.trim();
    const asesorNombre = (item.asesor || `${item.asesor_de_credito__nombre || ''} ${item.asesor_de_credito__apellido || ''}`).trim() || 'SIN ASESOR';

    mesesSet.add(mesLabel);
    asesoresSet.add(asesorNombre);
    lookupMap.set(`${mesLabel}_${asesorNombre}`, item.total);

    return { mesFormateado: mesLabel, nombreCompleto: asesorNombre, total: item.total };
  });

  const labels = Array.from(mesesSet);
  const asesores = Array.from(asesoresSet);

  const datasets = asesores.map((asesor, idx) => ({
    label: asesor,
    data: labels.map(mesLabel => lookupMap.get(`${mesLabel}_${asesor}`) || 0),
    backgroundColor: (colorPalette[idx % colorPalette.length]) + 'CC',
    borderColor: colorPalette[idx % colorPalette.length],
    borderWidth: 1
  }));

  createChart('clientesAsesorChart', {
    type: 'bar', 
    data: { labels, datasets },
    options: { responsive: true, maintainAspectRatio: false, scales: { x: { stacked: true }, y: { stacked: true } } }
  });

  renderTableData('tablaClientesAsesor', dataProcesada.map(i => [i.mesFormateado, i.nombreCompleto, i.total]));
}

async function tiposCredito() {
  const data = await fetchData('tipos-credito/');
  if (!data.length) return;

  createChart('tiposCreditoChart', {
    type: 'doughnut',
    data: {
      labels: data.map(i => i.tipo_credito),
      datasets: [{ data: data.map(i => i.cantidad), backgroundColor: colorPalette }]
    },
    options: { responsive: true, maintainAspectRatio: false }
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
      datasets: [{ data: data.map(i => i.cantidad), backgroundColor: colorPalette.slice().reverse() }]
    },
    options: { responsive: true, maintainAspectRatio: false }
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

  createChart('desembolsosChart', {
    type: 'line',
    data: {
      labels: dataProcesada.map(i => i.mesFormateado),
      datasets: [{ label: 'Desembolsos', data: dataProcesada.map(i => i.total), borderColor: '#10b981', fill: true }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  renderTableData('tablaDesembolsos', dataProcesada.map(i => [i.mesFormateado, i.total]));
}

async function recuperacion() {
  const data = await fetchData('recuperacion-mensual/');
  if (!data.length) return;

  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return { ...i, mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`, timestamp: fecha.getTime() };
  }).sort((a, b) => a.timestamp - b.timestamp);

  createChart('recuperacionChart', {
    type: 'bar',
    data: {
      labels: dataProcesada.map(i => i.mesFormateado),
      datasets: [
        { label: 'Mora', data: dataProcesada.map(i => i.mora), backgroundColor: '#ef4444' },
        { label: 'Interés', data: dataProcesada.map(i => i.interes), backgroundColor: '#f59e0b' },
        { label: 'Capital', data: dataProcesada.map(i => i.capital), backgroundColor: '#3b82f6' }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false, scales: { x: { stacked: true }, y: { stacked: true } } }
  });

  renderTableData('tablaRecuperacion', dataProcesada.map(i => [i.mesFormateado, formatCurrency(i.capital), formatCurrency(i.interes), formatCurrency(i.mora)]));
}

async function egresos() {
  const data = await fetchData('egresos-por-codigo-mes/');
  if (!data.length) return;

  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return { ...i, mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`, timestamp: fecha.getTime() };
  }).sort((a, b) => a.timestamp - b.timestamp);

  const labels = [...new Set(dataProcesada.map(i => i.mesFormateado))];
  const codigosUnicos = [...new Set(dataProcesada.map(i => i.codigo_egreso))];

  const datasets = codigosUnicos.map((codigo) => ({
    label: codigo,
    data: labels.map(mesLabel => {
      const registro = dataProcesada.find(i => i.mesFormateado === mesLabel && i.codigo_egreso === codigo);
      return registro ? registro.monto : 0;
    }),
    backgroundColor: `hsl(${Math.random() * 360}, 70%, 60%)`
  }));

  createChart('egresosChart', {
    type: 'bar',
    data: { labels, datasets },
    options: { responsive: true, maintainAspectRatio: false, scales: { x: { stacked: true }, y: { stacked: true } } }
  });

  renderTableData('tablaEgresos', dataProcesada.map(i => [i.mesFormateado, i.codigo_egreso, formatCurrency(i.monto)]));
}

async function bancos() {
  const data = await fetchData('bancos-por-mes/');
  if (!data.length) return;

  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return { ...i, mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`, timestamp: fecha.getTime() };
  }).sort((a, b) => a.timestamp - b.timestamp);

  createChart('bancosChart', {
    type: 'bar',
    data: {
      labels: dataProcesada.map(i => i.mesFormateado),
      datasets: [
        { label: 'Ingresos', data: dataProcesada.map(i => i.ingreso), backgroundColor: '#10b981' },
        { label: 'Egresos', data: dataProcesada.map(i => i.egreso), backgroundColor: '#ef4444' },
        { label: 'Saldos', type: 'line', data: dataProcesada.map(i => i.saldos), borderColor: '#3b82f6', fill: false }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  renderTableData('tablaBancos', dataProcesada.map(i => [i.mesFormateado, formatCurrency(i.ingreso), formatCurrency(i.egreso), formatCurrency(i.saldos)]));
}

async function acreedores() {
  const data = await fetchData('acreedores-por-mes/');
  if (!data.length) return;

  const dataProcesada = data.map(i => {
    const fecha = new Date(i.mes);
    return { ...i, mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`, timestamp: fecha.getTime() };
  }).sort((a, b) => a.timestamp - b.timestamp);

  createChart('acreedoresChart', {
    type: 'line',
    data: {
      labels: dataProcesada.map(i => i.mesFormateado),
      datasets: [
        { label: 'Pagos', data: dataProcesada.map(i => i.pagos), borderColor: '#3b82f6' },
        { label: 'Mora Pagada', data: dataProcesada.map(i => i.mora_pagada), borderColor: '#ef4444' },
        { label: 'Interés Pagado', data: dataProcesada.map(i => i.interes_pagado), borderColor: '#f59e0b' },
        { label: 'Aportes A Capital', data: dataProcesada.map(i => i.aporte_capital), borderColor: '#10b981' }
      ]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  renderTableData('tablaAcreedores', dataProcesada.map(i => [i.mesFormateado, formatCurrency(i.pagos), formatCurrency(i.mora_pagada), formatCurrency(i.interes_pagado), formatCurrency(i.aporte_capital)]));
}

async function morosidad() {
  const data = await fetchData('morosidad-por-mes/');
  if (!data.length) return;

  const dataProcesada = data.map(i => {
    const fecha = new Date(i.periodo);
    return { cantidad: i.cantidad, mesFormateado: `${labels_mes[fecha.getUTCMonth()]} ${fecha.getUTCFullYear()}`, timestamp: fecha.getTime() };
  }).sort((a, b) => a.timestamp - b.timestamp);

  createChart('morosidadChart', {
    type: 'line',
    data: {
      labels: dataProcesada.map(i => i.mesFormateado),
      datasets: [{ label: 'Clientes en Mora', data: dataProcesada.map(i => i.cantidad), borderColor: '#f43f5e', fill: true }]
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  renderTableData('tablaMorosidad', dataProcesada.map(i => [i.mesFormateado, i.cantidad]));
}

async function casos_exito_asesor() {
  const data = await fetchData('casos-exito-asesor/');
  if (!data.length) return;

  const labels = data.map(i => `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim());

  createChart('casosExitoChart', {
    type: 'bar',
    data: { 
      labels, 
      datasets: [
        { label: 'Total Otorgados', data: data.map(i => i.total_otorgados), backgroundColor: 'rgba(54, 162, 235, 0.5)' },
        { label: 'Cancelados (Éxito)', data: data.map(i => i.total_cancelados), backgroundColor: 'rgba(75, 192, 192, 0.8)' }
      ] 
    },
    options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false }
  });

  renderTableData('tablaCasosExito', data.map(i => [
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim(),
    i.total_otorgados,
    i.total_cancelados,
    ((i.total_cancelados / i.total_otorgados) * 100).toFixed(1) + '%'
  ]));
}

async function casos_judicial_asesor() {
  const data = await fetchData('casos-demanda-asesor/');
  if (!data.length) return;

  const labels = data.map(i => `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim());

  createChart('casosDemandaChart', {
    type: 'bar',
    data: { 
      labels, 
      datasets: [
        { label: 'Total Otorgados', data: data.map(i => i.total_otorgados), backgroundColor: 'rgba(54, 162, 235, 0.5)' },
        { label: 'Demandados', data: data.map(i => i.total_demandados), backgroundColor: 'rgba(239, 68, 68, 0.8)' }
      ] 
    },
    options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false }
  });

  renderTableData('tablaCasosDemanda', data.map(i => [
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim(),
    i.total_otorgados,
    i.total_demandados,
    ((i.total_demandados / i.total_otorgados) * 100).toFixed(1) + '%'
  ]));
}

async function casos_atraso_asesor() {
  const data = await fetchData('casos-atraso-asesor/');
  if (!data.length) return;

  const labels = data.map(i => `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim());

  createChart('casosAtrasadoChart', {
    type: 'bar',
    data: { 
      labels, 
      datasets: [
        { label: 'Total Otorgados', data: data.map(i => i.total_otorgados), backgroundColor: 'rgba(54, 162, 235, 0.5)' },
        { label: 'Atrasados', data: data.map(i => i.total_atrasados), backgroundColor: 'rgba(245, 158, 11, 0.8)' }
      ] 
    },
    options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false }
  });

  renderTableData('tablaCasosAtrasado', data.map(i => [
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim(),
    i.total_otorgados,
    i.total_atrasados,
    ((i.total_atrasados / i.total_otorgados) * 100).toFixed(1) + '%'
  ]));
}

async function cartera_asesor() {
  const data = await fetchData('cartera-asesor/');
  if (!data.length) return;

  const labels = data.map(i => `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim());

  createChart('carteraAsesorChart', {
    type: 'bar',
    data: { 
      labels, 
      datasets: [
        { label: 'Vigentes', data: data.map(i => i.saldo_cartera_total), backgroundColor: 'rgba(54, 162, 235, 0.5)' },
        { label: 'Atrasados', data: data.map(i => i.saldo_en_atraso), backgroundColor: 'rgba(239, 68, 68, 0.8)' }
      ] 
    },
    options: { responsive: true, maintainAspectRatio: false }
  });

  renderTableData('tablaCarteraAsesor', data.map(i => [
    `${i.asesor_de_credito__nombre || ''} ${i.asesor_de_credito__apellido || ''}`.trim(),
    formatCurrency(i.saldo_cartera_total),
    formatCurrency(i.saldo_en_atraso),
    ((i.saldo_en_atraso / i.saldo_cartera_total) * 100).toFixed(1) + '%'
  ]));
}

/* ===============================
   EXPORTACIÓN A PDF (FRONTEND)
=================================*/
function descargarPDF() {
  const elemento = document.getElementById('reporte-pdf');
  if (!elemento) return;

  const opciones = {
    margin:       [8, 8, 8, 8], // Márgenes superior, izquierdo, inferior, derecho en mm
    filename:     `dashboard_${new Date().toISOString().slice(0,10)}.pdf`,
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { 
      scale: 2, 
      useCORS: true, 
      logging: false,
      scrollY: 0, // Fuerza la captura desde el inicio del contenedor eliminando espacio en blanco
      scrollX: 0
    },
    pagebreak:    { mode: ['css', 'legacy'] },
    jsPDF:        { unit: 'mm', format: 'letter', orientation: 'portrait' }
  };

  html2pdf().set(opciones).from(elemento).save();
}

async function loadAllData() {
  showMessage('Cargando KPIs...');
  try {
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
  } catch (err) {
    console.error("Error cargando los KPIs:", err);
  } finally {
    // Se ejecuta siempre, garantizando la descarga tras cargar datos
    setTimeout(() => {
      descargarPDF();
    }, 800);
  }
}

window.onload = loadAllData;