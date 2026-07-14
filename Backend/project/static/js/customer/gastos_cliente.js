import { urls_p } from '../API/urls_api.js'
    /* =========================================================
   ESTADO Y CONFIGURACIÓN DE LA API
   ========================================================= */
// Eliminamos el arreglo estático de TIPOS_GASTO porque ahora vendrá de la base de datos
let tiposGastoDesdeApi = []; 
let gastos = [];
let nextId = 1;
let editingId = null;

const $ = (sel) => document.querySelector(sel);
const moneyFmt = new Intl.NumberFormat('es-GT', { style: 'currency', currency: 'GTQ' });

function formatMoney(n) {
  return moneyFmt.format(Number(n) || 0);
}

// Modificamos esta función para que busque en la lista que descargamos de la API
function tipoGastoName(id) {
  if (!id) return 'Sin clasificar';
  const t = tiposGastoDesdeApi.find((t) => t.id === Number(id));
  return t ? t.nombre : 'Sin clasificar';
}

/* =========================================================
   LLAMADA A LA API PARA OBTENER LOS TIPOS DE GASTO
   ========================================================= */
async function cargarTiposGasto() {
  const tipoSel = $('#tipoGasto');
  
  // URL de tu vista en Django que serializa el modelo TipoGasto (ej: JsonResponse)
  const URL_TIPOS_GASTO = urls_p.api_url_tipo_gasto; 

  try {
    const response = await fetch(URL_TIPOS_GASTO);
    if (!response.ok) throw new Error('No se pudieron obtener los tipos de gasto.');
    
    // Guardamos la respuesta en nuestra variable global
    tiposGastoDesdeApi = await response.json();

    // Poblamos el elemento <select> dinámicamente
    tiposGastoDesdeApi.forEach((t) => {
      // Usamos t.id y t.nombre que coinciden con los campos de tu modelo en Django
      tipoSel.add(new Option(t.nombre, t.id));
    });

  } catch (error) {
    console.error('Error al cargar tipos de gasto desde la API:', error);
    // Opción de respaldo por si la API falla temporalmente
    tipoSel.add(new Option('Error al cargar categorías...', ''));
  }
}

/* =========================================================
   INICIALIZAR NOMENCLATURA DE LA PÁGINA
   ========================================================= */
function initPage() {
  // Llamamos a la función asíncrona para traer los datos del backend
  cargarTiposGasto();

  // Capturar nombre del cliente desde el input hidden asignado por Django
  const currentCustomerName = $('#customer_name_hdn')?.value || 'Cliente Seleccionado';
  $('#receiptCustomerName').textContent = currentCustomerName;
}

/* =========================================================
   VALIDACIÓN
   ========================================================= */
function setFieldError(fieldEl, hasError) {
  fieldEl.classList.toggle('invalid', hasError);
}

function validateForm() {
  let valid = true;

  const montoField = $('#monto').closest('.field');
  const montoVal = parseFloat($('#monto').value);
  if (!montoVal || montoVal <= 0) {
    setFieldError(montoField, true);
    valid = false;
  } else {
    setFieldError(montoField, false);
  }

  return valid;
}

/* =========================================================
   FORMULARIO: Frecuencia "Otro"
   ========================================================= */
$('#frecuencia').addEventListener('change', (e) => {
  const wrap = $('#frecuenciaOtroWrap');
  wrap.classList.toggle('hidden', e.target.value !== 'Otro');
});

/* =========================================================
   ACCIONES LOCALES (C-U-D MEMORIA)
   ========================================================= */
function resetForm() {
  $('#gastoForm').reset();
  $('#gastoId').value = '';
  $('#frecuenciaOtroWrap').classList.add('hidden');
  $('#frecuencia').value = 'Único';
  editingId = null;
  $('#submitBtn').textContent = 'Añadir al Recibo';
  $('#cancelEdit').hidden = true;
  setFieldError($('#monto').closest('.field'), false);
}

function getFrecuenciaValue() {
  const base = $('#frecuencia').value;
  if (base === 'Otro') {
    return $('#frecuenciaOtro').value.trim() || 'Otro';
  }
  return base;
}

$('#gastoForm').addEventListener('submit', (e) => {
  e.preventDefault();
  if (!validateForm()) return;

  // Forzamos la conversión a entero para cumplir con las llaves foráneas del modelo Django
  const customerId = parseInt($('#customer_id').value, 10);
  const tipoGastoVal = $('#tipoGasto').value;
  const tipoGastoId = tipoGastoVal ? parseInt(tipoGastoVal, 10) : null;

  const payload = {
    id: editingId ?? nextId++,
    customer: isNaN(customerId) ? null : customerId, // Se envía como Integer
    tipo_gasto: isNaN(tipoGastoId) ? null : tipoGastoId, // Se envía como Integer o null si es "Sin clasificar"
    descripcion: $('#descripcion').value.trim(),
    monto: parseFloat($('#monto').value),
    frecuencia: getFrecuenciaValue(),
    observaciones: $('#observaciones').value.trim(),
  };

  if (editingId) {
    const idx = gastos.findIndex((g) => g.id === editingId);
    gastos[idx] = payload;
  } else {
    gastos.push(payload);
  }

  resetForm();
  renderReceipt();
});

$('#cancelEdit').addEventListener('click', resetForm);

function startEdit(id) {
  const g = gastos.find((g) => g.id === id);
  if (!g) return;

  editingId = id;
  $('#gastoId').value = id;
  $('#tipoGasto').value = g.tipo_gasto || '';
  $('#descripcion').value = g.descripcion || '';
  $('#monto').value = g.monto;
  $('#observaciones').value = g.observaciones || '';

  const knownFreqs = ['Único', 'Diario', 'Semanal', 'Quincenal', 'Mensual', 'Anual'];
  if (knownFreqs.includes(g.frecuencia)) {
    $('#frecuencia').value = g.frecuencia;
    $('#frecuenciaOtroWrap').classList.add('hidden');
  } else {
    $('#frecuencia').value = 'Otro';
    $('#frecuenciaOtroWrap').classList.remove('hidden');
    $('#frecuenciaOtro').value = g.frecuencia;
  }

  $('#submitBtn').textContent = 'Guardar cambios';
  $('#cancelEdit').hidden = false;
  $('#gastoForm').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function deleteGasto(id) {
  gastos = gastos.filter((g) => g.id !== id);
  if (editingId === id) resetForm();
  renderReceipt();
}

/* =========================================================
   RENDERIZACIÓN DEL RECIBO ÚNICO
   ========================================================= */
function renderReceipt() {
  $('#receiptDate').textContent = new Date().toLocaleDateString('es-GT', {
    day: '2-digit', month: 'short', year: 'numeric',
  });
  $('#receiptCount').textContent = `${gastos.length} partida${gastos.length === 1 ? '' : 's'}`;

  const itemsEl = $('#receiptItems');
  itemsEl.innerHTML = '';

  if (gastos.length === 0) {
    itemsEl.innerHTML = `
      <li class="receipt-empty">
        <strong>Aún no hay gastos en esta tanda</strong>
        Usa el formulario de la izquierda para anexar elementos.
      </li>`;
    $('#btnGuardarApi').disabled = true;
  } else {
    const tpl = $('#itemTemplate');
    gastos
      .slice()
      .sort((a, b) => b.id - a.id)
      .forEach((g) => {
        const node = tpl.content.cloneNode(true);
        const li = node.querySelector('.receipt-item');
        li.dataset.id = g.id;
        li.querySelector('.receipt-item__type').textContent = tipoGastoName(g.tipo_gasto);
        li.querySelector('.receipt-item__desc').textContent = g.descripcion || 'Sin descripción';
        li.querySelector('.receipt-item__amount').textContent = formatMoney(g.monto);
        li.querySelector('.receipt-item__freq').textContent = g.frecuencia;
        li.querySelector('.icon-btn--edit').addEventListener('click', () => startEdit(g.id));
        li.querySelector('.icon-btn--del').addEventListener('click', () => deleteGasto(g.id));
        itemsEl.appendChild(li);
      });
    $('#btnGuardarApi').disabled = false;
  }

  const total = gastos.reduce((sum, g) => sum + Number(g.monto), 0);
  $('#receiptTotal').textContent = formatMoney(total);
}

/* =========================================================
   ENVÍO POST DE LA INFORMACIÓN AL BACKEND / API
   ========================================================= */
$('#btnGuardarApi').addEventListener('click', async () => {
    if (gastos.length === 0) return;

    const btn = $('#btnGuardarApi');
    btn.disabled = true;
    btn.textContent = 'Enviando información...';

    const URL_API = urls_p.api_url_gastos_cliente;

    try {

        for (const gasto of gastos) {

            const response = await fetch(URL_API, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    customer: gasto.customer,
                    tipo_gasto: gasto.tipo_gasto,
                    descripcion: gasto.descripcion,
                    monto: gasto.monto,
                    frecuencia: gasto.frecuencia,
                    observaciones: gasto.observaciones
                })
            });

            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(
                    errData.detail ||
                    JSON.stringify(errData) ||
                    'Error al registrar un gasto.'
                );
            }
        }

        Swal.fire({
            icon: "success",
            title: "Registro Completado",
            text: "Todos los gastos fueron registrados correctamente.",
            timer: 5000,
            showConfirmButton: false,
        });

        gastos = [];
        resetForm();
        renderReceipt();
        let codigo_cliente = document.getElementById('codigo_cliente').value;
        setTimeout(() => { window.location.href = `/customer/checklist/${codigo_cliente}/`; }, 1000);

    } catch (error) {

        console.error(error);

        Swal.fire({
            icon: "error",
            title: "Error",
            text: error.message,
            timer: 7000,
            showConfirmButton: false,
        });

    } finally {

        btn.disabled = false;
        btn.textContent = 'Guardar Todo en la Base de Datos';

    }
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/* =========================================================
   INIT
   ========================================================= */
initPage();
renderReceipt();
