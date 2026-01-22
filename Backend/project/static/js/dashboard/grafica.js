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
  

  
  const labels = data.map(i => i.mes);
  const values = data.map(i => i.total);

  createChart('clientesMesChart', {
    type: 'line',
    data: { labels, datasets: [{ label: 'Clientes', data: values, fill: true }] },
    options: { responsive: true, maintainAspectRatio: false }
  });

  document.getElementById('totalClientes').textContent =
    values.reduce((a,b)=>a+b,0).toLocaleString();
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
    casos_exito_asesor()
  ]);
  showMessage('Dashboard actualizado ✅');
}

window.onload = loadAllData;