import { urls_p } from '../API/urls_api.js';

// ==========================================================================
// ESTADO GLOBAL DEL MÓDULO DE PLAN DE INVERSIÓN
// ==========================================================================
let guaranteeList = [];
let fiadoresGarantiasMap = {};

const tipoDocumento = document.getElementById("tipo_documento");
const tipoPagare = document.getElementById("tipo_pagare");
const claseDocumento = document.getElementById("clase_de_documento");
const contenedorPagare = document.getElementById("contenedor_pagare");
const contenedorClaseDocumento = document.getElementById("contenedor_clase_documento");
const contenedorFiadores = document.getElementById("contenedor_fiadores");
const contenedorCreditos = document.getElementById("contenedor_creditos");
const contenedorNotariosDoc = document.getElementById("contenedor_notarios_doc");
const notarioDocSelect = $("#notario_documentacion");
const formaPago = document.getElementById("forma_de_pago");
const contenedorPlazoGarantia = document.getElementById("contenedor_plazo_garantia");

// ==========================================================================
// TOAST NOTIFICATIONS HELPER
// ==========================================================================
function showToast(message, icon = 'info') {
    if (typeof Swal !== 'undefined' && Swal.mixin) {
        const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 2800,
            timerProgressBar: true
        });
        Toast.fire({
            icon: icon,
            title: message
        });
    } else {
        console.log(`[${icon.toUpperCase()}] ${message}`);
    }
}

// ==========================================================================
// SEGURIDAD: VERIFICACIÓN DE CÓDIGO ADMINISTRATIVO
// ==========================================================================
async function verificarCodigoSeguridad() {
    const result = await Swal.fire({
        title: 'Autorización Requerida',
        text: "Para registrar un crédito en estado ACEPTADO/APROBADO, ingrese el código de seguridad enviado al administrador:",
        input: 'password',
        inputAttributes: {
            autocapitalize: 'off',
            autocorrect: 'off'
        },
        showCancelButton: true,
        confirmButtonText: 'Verificar y Guardar',
        confirmButtonColor: '#BA181B',
        cancelButtonText: 'Cancelar',
        showLoaderOnConfirm: true,
        preConfirm: async (codigoIngresado) => {
            try {
                const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
                const csrfToken = csrfTokenElement ? csrfTokenElement.getAttribute('content') : '';

                const response = await fetch('/financings/validar-codigo-seguridad/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ codigo: codigoIngresado })
                });

                if (!response.ok) {
                    throw new Error('Error de validación en el servidor');
                }
                return await response.json();
            } catch (error) {
                Swal.showValidationMessage(`Error de autorización: ${error.message}`);
            }
        },
        allowOutsideClick: () => !Swal.isLoading()
    });

    if (result.isConfirmed) {
        if (result.value && result.value.valido) {
            Swal.fire({
                title: '¡Autorizado!',
                text: 'Código de seguridad verificado correctamente.',
                icon: 'success',
                timer: 1400,
                showConfirmButton: false
            });
            await new Promise(resolve => setTimeout(resolve, 900));
            return true;
        } else {
            Swal.fire('Acceso Denegado', 'El código de seguridad ingresado es incorrecto.', 'error');
            return false;
        }
    }
    return false;
}

// ==========================================================================
// PERSISTENCIA API (POST / PUT)
// ==========================================================================
export async function savePlanInversion(formData, planId = null) {
    try {
        const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
        if (!csrfTokenElement) throw new Error('CSRF token not found');
        const csrfToken = csrfTokenElement.getAttribute('content');

        const urlFinal = planId ? `${urls_p.api_url_investment_plan}${planId}/` : urls_p.api_url_investment_plan;
        const metodo = planId ? 'put' : 'post';

        const response = await axios({
            method: metodo,
            url: urlFinal,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            data: formData
        });

        return response.data;
    } catch (error) {
        console.error(`Error en la operación ${planId ? 'PUT' : 'POST'}:`, error.response?.data || error.message);
        throw error;
    }
}

// ==========================================================================
// INICIALIZACIÓN DE SELECT2 EN NOTARIOS Y CHECK DE NOTIFICACIÓN
// ==========================================================================
function inicializarSelect2Notario($element, placeholder = 'Seleccione Notario', dropdownParent = null) {
    const config = {
        width: '100%',
        ajax: {
            url: urls_p.api_url_notario,
            dataType: 'json',
            delay: 250,
            data: function (params) { return { term: params.term }; },
            processResults: function (data) {
                return {
                    results: (Array.isArray(data) ? data : []).map(item => ({
                        id: item.id,
                        text: item.nombre_completo || item.nombre || `${item.first_name || ''} ${item.last_name || ''}`.trim() || `Usuario #${item.id}`
                    }))
                };
            },
            cache: true
        },
        placeholder: placeholder,
        allowClear: true
    };
    if (dropdownParent) {
        config.dropdownParent = dropdownParent;
    }
    $element.select2(config);
}

function toggleCheckNotificarNotario($selectEl, $checkContainer) {
    if (!$selectEl.length || !$checkContainer.length) return;
    if ($selectEl.val()) {
        $checkContainer.fadeIn(180);
    } else {
        $checkContainer.fadeOut(150);
    }
}

if (notarioDocSelect.length) {
    inicializarSelect2Notario(notarioDocSelect, 'Seleccione al Notario Responsable');
    notarioDocSelect.on('change select2:select select2:clear', function () {
        toggleCheckNotificarNotario(notarioDocSelect, $("#contenedor_notificar_notario_doc"));
    });
}

inicializarSelect2Notario($("#garantia_notario_builder"), 'Seleccione Notario para esta Garantía');
$("#garantia_notario_builder").on('change select2:select select2:clear', function () {
    toggleCheckNotificarNotario($("#garantia_notario_builder"), $("#contenedor_notificar_notario_garantia"));
});

inicializarSelect2Notario($("#modal_garantia_notario"), 'Seleccione Notario para esta Garantía', $('#modalEditarGarantia'));
$("#modal_garantia_notario").on('change select2:select select2:clear', function () {
    toggleCheckNotificarNotario($("#modal_garantia_notario"), $("#modal_contenedor_notificar_notario"));
});

// ==========================================================================
// DINAMISMO: FORMA DE PAGO Y PLAZO DE GRACIA
// ==========================================================================
if (formaPago && contenedorPlazoGarantia) {
    formaPago.addEventListener("change", () => {
        const valor = formaPago.value;
        if (valor === "INTERES MENSUAL Y CAPITAL AL VENCIMIENTO" || valor === "INTERES Y CAPITAL AL VENCIMIENTO") {
            $(contenedorPlazoGarantia).fadeIn(250);
        } else {
            $(contenedorPlazoGarantia).fadeOut(200);
            const plazoGarantiaInput = document.getElementById("plazo_garantia");
            if (plazoGarantiaInput) plazoGarantiaInput.value = "";
        }
    });
}

// ==========================================================================
// DINAMISMO: DOCUMENTACIÓN LEGAL (PAGARÉ, RECONOCIMIENTO DE DEUDA, ACTA, FIADORES, NOTARIOS)
// ==========================================================================
function actualizarVisibilidadDocumento() {
    if (!tipoDocumento) return;
    const docSeleccionado = tipoDocumento.value;

    if (contenedorPagare) contenedorPagare.style.display = "none";
    if (contenedorClaseDocumento) contenedorClaseDocumento.style.display = "none";
    if (contenedorFiadores) contenedorFiadores.style.display = "block";
    if (contenedorCreditos) contenedorCreditos.style.display = "block";
    if (contenedorNotariosDoc) contenedorNotariosDoc.style.display = "none";

    if (docSeleccionado === "PAGARE") {
        if (contenedorPagare) $(contenedorPagare).fadeIn(200);
        if (claseDocumento) claseDocumento.value = "";
        actualizarVisibilidadPagare();
    } else if (docSeleccionado === "RECONOCIMIENTO DE DEUDA") {
        if (contenedorClaseDocumento) $(contenedorClaseDocumento).fadeIn(200);
        if (contenedorNotariosDoc) $(contenedorNotariosDoc).fadeIn(200);
    } else if (docSeleccionado === "ACTA") {
        if (claseDocumento) claseDocumento.value = "";
        if (contenedorNotariosDoc) $(contenedorNotariosDoc).fadeIn(200);
    } else {
        if (claseDocumento) claseDocumento.value = "";
    }
}

function actualizarVisibilidadPagare() {
    if (!tipoPagare) return;
    const valorPagare = (tipoPagare.value || "").toUpperCase();

    if (valorPagare.includes("FIADOR")) {
        if (contenedorFiadores) $(contenedorFiadores).fadeIn(200);
    }
    if (valorPagare.includes("REESTRUCTURACION") || valorPagare.includes("RESTRUCTURACION")) {
        if (contenedorCreditos) $(contenedorCreditos).fadeIn(200);
    }
}

if (tipoDocumento) tipoDocumento.addEventListener("change", actualizarVisibilidadDocumento);
if (tipoPagare) tipoPagare.addEventListener("change", actualizarVisibilidadPagare);

// ==========================================================================
// AGREGAR FIADORES DINÁMICOS CON REGISTRO DE GARANTÍAS PROPIAS
// ==========================================================================
function renderDynamicFiadorFields(filaId) {
    const $fila = $(`#${filaId}`);
    if (!$fila.length) return;

    const tipo = $fila.find('.fiador-gar-tipo').val();
    const $containerWrap = $fila.find('.fiador-dynamic-fields-container');
    const $fieldsContainer = $fila.find('.fiador-dynamic-fields');
    $fila.find('.fiador-spec-tipo-nombre').text(tipo || '');

    const estado = ($("#estado_aprobacion").val() || "").toUpperCase();
    if (estado !== "ACEPTADO") {
        $containerWrap.hide();
        $fieldsContainer.empty();
        return;
    }

    $containerWrap.show();
    $fieldsContainer.html(generarHTMLCamposEspecificacion(tipo, `${filaId}_spec_`));
}

function evaluarNotarioFiadorBuilder(filaId) {
    const $fila = $(`#${filaId}`);
    if (!$fila.length) return;

    const tipo = $fila.find('.fiador-gar-tipo').val();
    const valor = parseFloat($fila.find('.fiador-gar-valor').val()) || 0;
    const $notarioWrap = $fila.find('.fiador-gar-notario-wrap');
    const $notarioSelect = $fila.find('.fiador-gar-notario');

    if (tipo === "CHEQUE / PAGARE" && valor > 500) {
        $notarioWrap.fadeIn(180);
    } else {
        $notarioWrap.fadeOut(150);
        $notarioSelect.val(null).trigger('change');
    }
}

function renderFiadorGuarantees(filaId) {
    const $fila = $(`#${filaId}`);
    if (!$fila.length) return;

    const lista = fiadoresGarantiasMap[filaId] || [];
    const $container = $fila.find('.fiador-lista-garantias');
    const $badge = $fila.find('.fiador-garantias-count');
    const estadoAprobado = ($("#estado_aprobacion").val() || "").toUpperCase() === "ACEPTADO";

    $badge.text(`${lista.length} garantía${lista.length === 1 ? '' : 's'}`);
    $badge.toggleClass('bg-danger', lista.length > 0).toggleClass('bg-secondary', lista.length === 0);

    if (lista.length === 0) {
        $container.html(`
            <div class="text-center text-muted small py-2 border rounded-3 bg-white bg-opacity-50">
                <i class="bi bi-shield-plus me-1"></i> Aún no se han agregado garantías para este fiador.
            </div>
        `);
        return;
    }

    $container.empty();

    lista.forEach((g, index) => {
        const notarioText = (g.notario && g.notario.nombre) ? g.notario.nombre : null;
        const notarioNotifyBadge = (g.notario && g.notario.id)
            ? (g.notario.notificar !== false
                ? `<span class="badge bg-success-subtle text-success border border-success-subtle ms-1"><i class="bi bi-envelope-check"></i> Notificar</span>`
                : `<span class="badge bg-secondary-subtle text-secondary border border-secondary-subtle ms-1"><i class="bi bi-envelope-slash"></i> Sin notificación</span>`)
            : '';

        const specs = g.especificaciones || {};
        const keys = Object.keys(specs);
        const hasSpecs = keys.some(k => specs[k] !== null && specs[k] !== '' && specs[k] !== undefined);

        let statusBadgeSpecsHTML = '';
        if (estadoAprobado) {
            if (hasSpecs) {
                statusBadgeSpecsHTML = `<span class="badge-specs-complete ms-1"><i class="bi bi-check-circle-fill"></i> Especificaciones completadas</span>`;
            } else {
                statusBadgeSpecsHTML = `<span class="badge-specs-pending ms-1"><i class="bi bi-exclamation-triangle-fill"></i> Especificaciones pendientes</span>`;
            }
        }

        let specsBadgesHTML = '';
        if (hasSpecs) {
            specsBadgesHTML = Object.entries(specs)
                .filter(([_, val]) => val !== null && val !== '' && val !== undefined)
                .map(([key, val]) => `
                    <div class="spec-chip">
                        <span class="spec-key">${key.replace(/_/g, ' ')}</span>
                        <span class="spec-val">${val}</span>
                    </div>
                `).join('');
        }

        const cardHTML = $(`
            <div class="guarantee-item-card fiador-guarantee-item animate-fade-in mb-2 p-3" data-fila-id="${filaId}" data-index="${index}">
                <div class="d-flex justify-content-between align-items-start gap-2 flex-wrap">
                    <div>
                        <div class="d-flex align-items-center flex-wrap gap-1">
                            <span class="guarantee-tag">
                                <i class="bi bi-shield-shaded me-1"></i> ${g.tipo}
                            </span>
                            <span class="badge bg-dark-subtle text-dark border">Garantía de Fiador</span>
                            ${statusBadgeSpecsHTML}
                        </div>
                        <h6 class="fw-bold text-dark mb-1 mt-1 small">${g.descripcion || 'Sin descripción'}</h6>
                        <span class="text-xs text-muted">
                            Cobertura: <strong class="text-dark font-monospace">${formatearMonedaQ(g.valor)}</strong>
                            ${notarioText ? `&nbsp;|&nbsp; <span class="badge bg-secondary"><i class="bi bi-person-fill"></i> Notario: ${notarioText}</span>${notarioNotifyBadge}` : ''}
                        </span>
                    </div>
                    <div class="text-end d-flex align-items-center gap-1">
                        <button type="button" class="btn btn-sm ${estadoAprobado && !hasSpecs ? 'btn-danger btn-completar-pulsing text-white' : 'btn-outline-primary'} btn-editar-garantia-fiador" data-fila-id="${filaId}" data-index="${index}" title="Modificar Garantía del Fiador">
                            <i class="bi bi-pencil-square"></i> ${estadoAprobado && !hasSpecs ? 'Completar' : 'Modificar'}
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-danger btn-remover-garantia-fiador" data-fila-id="${filaId}" data-index="${index}" title="Quitar Garantía del Fiador">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
                ${hasSpecs && specsBadgesHTML ? `
                    <div class="mt-2">
                        <a href="javascript:void(0);" class="btn-toggle-specs small text-primary text-decoration-none fw-bold" style="font-size: 0.75rem;">
                            <i class="bi bi-chevron-down"></i> Ver Especificaciones (${Object.keys(specs).length} campos)
                        </a>
                        <div class="specs-detail-grid mt-2" style="display: none;">
                            ${specsBadgesHTML}
                        </div>
                    </div>
                ` : ''}
            </div>
        `);

        $container.append(cardHTML);
    });
}

function agregarFilaFiador(idPreload = null, textPreload = null, garantiasPreload = []) {
    const filaId = 'fiador_' + Date.now() + '_' + Math.floor(Math.random() * 1000);
    fiadoresGarantiasMap[filaId] = [];

    const nuevaFila = $(`
        <div class="fila-fiador fiador-card mb-3" id="${filaId}">
            <div class="row align-items-center g-2">
                <div class="col-10 col-md-11">
                    <select class="form-control fiador_select customer_id" style="width: 100%;"></select>
                </div>
                <div class="col-2 col-md-1">
                    <button type="button" class="btn btn-outline-danger w-100 btn-eliminar-fiador" data-fila-id="${filaId}" title="Quitar Fiador">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>

            <!-- Opción para habilitar registro de garantías del fiador (se habilita al seleccionar fiador) -->
            <div class="fiador-garantia-toggle-wrapper mt-2 pt-2 border-top" style="display: none;">
                <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
                    <div class="form-check form-switch d-flex align-items-center gap-2 mb-0">
                        <input class="form-check-input toggle-fiador-garantia" type="checkbox" role="switch" id="toggle_gar_${filaId}" data-fila-id="${filaId}">
                        <label class="form-check-label fw-semibold text-dark small" for="toggle_gar_${filaId}">
                            <i class="bi bi-shield-lock-fill text-danger me-1"></i> ¿Este fiador deja registro de garantía?
                        </label>
                    </div>
                    <span class="badge bg-secondary rounded-pill fiador-garantias-count">0 garantías</span>
                </div>

                <!-- Panel de Garantías del Fiador -->
                <div class="fiador-garantias-panel mt-3" style="display: none;">
                    <div class="fiador-guarantee-builder p-3 rounded-3 border bg-white bg-opacity-75 mb-3">
                        <h6 class="fw-bold small text-dark mb-2">
                            <i class="bi bi-plus-circle-fill text-danger me-1"></i> Registrar Garantía del Fiador
                        </h6>
                        <div class="row g-2">
                            <div class="col-md-4">
                                <label class="form-label-custom">Tipo de Garantía <span class="req">*</span></label>
                                <select class="form-control glass-select fiador-gar-tipo" data-fila-id="${filaId}">
                                    <option value="HIPOTECA">HIPOTECA</option>
                                    <option value="DERECHO DE POSESION HIPOTECA">DERECHO DE POSESION HIPOTECA</option>
                                    <option value="CHEQUE / PAGARE">CHEQUE / PAGARE</option>
                                    <option value="VEHICULO">VEHICULO</option>
                                    <option value="MOBILIARIA">MOBILIARIA</option>
                                </select>
                            </div>
                            <div class="col-md-5">
                                <label class="form-label-custom">Descripción / Resumen <span class="req">*</span></label>
                                <input type="text" class="form-control glass-input fiador-gar-desc" placeholder="Ej. Inmueble o vehículo propiedad del fiador...">
                            </div>
                            <div class="col-md-3">
                                <label class="form-label-custom">Valor Cobertura (Q) <span class="req">*</span></label>
                                <div class="input-group">
                                    <span class="input-group-text bg-white border-end-0 fw-bold text-muted">Q</span>
                                    <input type="number" step="0.01" class="form-control glass-input border-start-0 fiador-gar-valor" data-fila-id="${filaId}" placeholder="0.00">
                                </div>
                            </div>

                            <!-- Notario condicional para Cheque/Pagaré > 500 -->
                            <div class="col-md-6 fiador-gar-notario-wrap" style="display: none;">
                                <label class="form-label-custom text-danger">
                                    <i class="bi bi-person-check-fill"></i> Notario Asignado a esta Garantía
                                </label>
                                <select class="form-control glass-select fiador-gar-notario" style="width: 100%;"></select>
                                <div class="fiador-gar-notificar-wrap notario-notify-box mt-2" style="display: none;">
                                    <div class="form-check form-switch d-flex align-items-center gap-2 mb-0">
                                        <input class="form-check-input fiador-gar-notificar" type="checkbox" role="switch" id="notificar_fgar_${filaId}" checked>
                                        <label class="form-check-label fw-semibold text-dark small" for="notificar_fgar_${filaId}">
                                            <i class="bi bi-envelope-check-fill text-danger me-1"></i> Notificar al notario
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Especificaciones dinámicas si estado === ACEPTADO -->
                        <div class="fiador-dynamic-fields-container dynamic-fields-wrapper mt-3" style="display: none;">
                            <div class="dynamic-fields-header">
                                <i class="bi bi-file-earmark-ruled-fill"></i>
                                <span>Especificaciones Técnicas y Registrales (<strong class="fiador-spec-tipo-nombre">HIPOTECA</strong>)</span>
                            </div>
                            <div class="fiador-dynamic-fields row g-2"></div>
                        </div>

                        <div class="text-end mt-3">
                            <button type="button" class="btn-glass-secondary py-1 px-3 btn-agregar-garantia-fiador" data-fila-id="${filaId}">
                                <i class="bi bi-plus-lg"></i> Agregar Garantía al Fiador
                            </button>
                        </div>
                    </div>

                    <div class="fiador-lista-garantias"></div>
                </div>
            </div>
        </div>
    `);

    $("#lista_fiadores").append(nuevaFila);

    const selectEl = nuevaFila.find('.fiador_select');
    selectEl.select2({
        width: '100%',
        ajax: {
            url: urls_p.api_url_cliente,
            dataType: 'json',
            delay: 250,
            data: function (params) { return { term: params.term }; },
            processResults: function (data) {
                if (Array.isArray(data)) {
                    return {
                        results: data.map(item => ({
                            id: item.id,
                            text: `${item.customer_code} - ${item.first_name} ${item.last_name}`
                        }))
                    };
                }
                return { results: [] };
            },
            cache: true
        },
        placeholder: 'Buscar cliente por nombre o código...',
        minimumInputLength: 1,
        allowClear: true
    });

    // Inicializar Select2 del notario para garantías de este fiador
    const $notarioFiadorSelect = nuevaFila.find('.fiador-gar-notario');
    inicializarSelect2Notario($notarioFiadorSelect, 'Seleccione Notario para esta Garantía');
    $notarioFiadorSelect.on('change select2:select select2:clear', function () {
        toggleCheckNotificarNotario($notarioFiadorSelect, nuevaFila.find('.fiador-gar-notificar-wrap'));
    });

    // Mostrar/ocultar opción de garantía al seleccionar o limpiar fiador
    selectEl.on('change select2:select select2:clear', function () {
        const val = $(this).val();
        const $toggleWrap = nuevaFila.find('.fiador-garantia-toggle-wrapper');
        if (val) {
            $toggleWrap.slideDown(200);
        } else {
            $toggleWrap.slideUp(180);
            nuevaFila.find('.toggle-fiador-garantia').prop('checked', false);
            nuevaFila.find('.fiador-garantias-panel').hide();
            fiadoresGarantiasMap[filaId] = [];
            renderFiadorGuarantees(filaId);
            actualizarMonitorCobertura();
        }
    });

    if (idPreload) {
        const option = new Option(textPreload || `Cliente #${idPreload}`, idPreload, true, true);
        selectEl.append(option).trigger('change');
    }

    if (Array.isArray(garantiasPreload) && garantiasPreload.length > 0) {
        fiadoresGarantiasMap[filaId] = garantiasPreload.map(g => ({
            id: Date.now() + Math.floor(Math.random() * 10000),
            tipo: g.tipo,
            descripcion: g.descripcion,
            valor: parseFloat(g.valor) || 0,
            notario: g.notario || null,
            especificaciones: g.especificaciones || {}
        }));
        nuevaFila.find('.toggle-fiador-garantia').prop('checked', true);
        nuevaFila.find('.fiador-garantias-panel').show();
        renderDynamicFiadorFields(filaId);
        renderFiadorGuarantees(filaId);
        actualizarMonitorCobertura();
    } else {
        renderFiadorGuarantees(filaId);
    }
}

$("#btnAgregarFiador").click(function () {
    agregarFilaFiador();
});

// Eventos delegados para garantías de fiadores
$(document).on('click', '.btn-eliminar-fiador', function () {
    const filaId = $(this).data('fila-id');
    delete fiadoresGarantiasMap[filaId];
    $(this).closest('.fila-fiador').remove();
    actualizarMonitorCobertura();
});

$(document).on('change', '.toggle-fiador-garantia', function () {
    const filaId = $(this).data('fila-id');
    const $fila = $(`#${filaId}`);
    const $panel = $fila.find('.fiador-garantias-panel');

    if ($(this).is(':checked')) {
        $panel.slideDown(220);
        renderDynamicFiadorFields(filaId);
    } else {
        $panel.slideUp(200);
        fiadoresGarantiasMap[filaId] = [];
        renderFiadorGuarantees(filaId);
        actualizarMonitorCobertura();
    }
});

$(document).on('change', '.fiador-gar-tipo', function () {
    const filaId = $(this).data('fila-id');
    renderDynamicFiadorFields(filaId);
    evaluarNotarioFiadorBuilder(filaId);
});

$(document).on('keyup change', '.fiador-gar-valor', function () {
    const filaId = $(this).data('fila-id');
    evaluarNotarioFiadorBuilder(filaId);
});

$(document).on('click', '.btn-agregar-garantia-fiador', function () {
    const filaId = $(this).data('fila-id');
    const $fila = $(`#${filaId}`);
    if (!$fila.length) return;

    const tipo = $fila.find('.fiador-gar-tipo').val();
    const descripcion = ($fila.find('.fiador-gar-desc').val() || "").trim();
    const valor = parseFloat($fila.find('.fiador-gar-valor').val()) || 0;
    const estado = ($("#estado_aprobacion").val() || "").toUpperCase();

    if (!tipo) {
        Swal.fire('Atención', 'Seleccione el tipo de garantía del fiador.', 'warning');
        return;
    }
    if (!descripcion) {
        Swal.fire('Atención', 'Ingrese la descripción de la garantía del fiador.', 'warning');
        $fila.find('.fiador-gar-desc').focus();
        return;
    }
    if (valor <= 0) {
        Swal.fire('Atención', 'Ingrese un valor de cobertura válido superior a Q 0.00.', 'warning');
        $fila.find('.fiador-gar-valor').focus();
        return;
    }

    let notarioGarantia = null;
    const $notarioSelect = $fila.find('.fiador-gar-notario');
    if (tipo === "CHEQUE / PAGARE" && valor > 500 && $notarioSelect.val()) {
        notarioGarantia = {
            id: parseInt($notarioSelect.val()),
            nombre: $notarioSelect.find('option:selected').text(),
            notificar: $fila.find('.fiador-gar-notificar').is(':checked')
        };
    }

    let especificaciones = {};
    if (estado === "ACEPTADO") {
        especificaciones = extraerEspecificacionesGenerico(tipo, `${filaId}_spec_`);
    }

    if (!Array.isArray(fiadoresGarantiasMap[filaId])) {
        fiadoresGarantiasMap[filaId] = [];
    }

    fiadoresGarantiasMap[filaId].push({
        id: Date.now() + Math.floor(Math.random() * 1000),
        tipo: tipo,
        descripcion: descripcion,
        valor: valor,
        notario: notarioGarantia,
        especificaciones: especificaciones
    });

    // Resetear inputs del creador de garantía del fiador
    $fila.find('.fiador-gar-desc').val('');
    $fila.find('.fiador-gar-valor').val('');
    $notarioSelect.val(null).trigger('change');
    $fila.find('.fiador-gar-notificar').prop('checked', true);
    renderDynamicFiadorFields(filaId);
    evaluarNotarioFiadorBuilder(filaId);

    renderFiadorGuarantees(filaId);
    actualizarMonitorCobertura();
    showToast('Garantía del fiador agregada exitosamente.', 'success');
});

$(document).on('click', '.btn-remover-garantia-fiador', function () {
    const filaId = $(this).data('fila-id');
    const index = parseInt($(this).data('index'));
    if (fiadoresGarantiasMap[filaId] && !isNaN(index) && index >= 0 && index < fiadoresGarantiasMap[filaId].length) {
        fiadoresGarantiasMap[filaId].splice(index, 1);
        renderFiadorGuarantees(filaId);
        actualizarMonitorCobertura();
        showToast('Garantía del fiador eliminada.', 'info');
    }
});

$(document).on('click', '.btn-editar-garantia-fiador', function () {
    const filaId = $(this).data('fila-id');
    const index = parseInt($(this).data('index'));
    abrirModalEdicionGarantia(index, filaId);
});

// ==========================================================================
// AGREGAR CRÉDITOS VIGENTES DINÁMICOS
// ==========================================================================
function agregarFilaCredito(idPreload = null, textPreload = null) {
    const filaId = 'credito_' + Date.now() + Math.floor(Math.random() * 100);
    const nuevaFila = $(`
        <div class="row mb-2 fila-credito align-items-center g-2" id="${filaId}">
            <div class="col-10 col-md-11">
                <select class="form-control credito_vigente" style="width: 100%;"></select>
            </div>
            <div class="col-2 col-md-1">
                <button type="button" class="btn btn-outline-danger w-100 btn-eliminar-item" title="Quitar Crédito">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        </div>
    `);

    $("#lista_creditos").append(nuevaFila);

    const selectEl = nuevaFila.find('.credito_vigente');
    selectEl.select2({
        width: '100%',
        ajax: {
            url: urls_p.api_url_credit_vigente,
            dataType: 'json',
            delay: 250,
            data: function (params) { return { term: params.term }; },
            processResults: function (data) {
                if (Array.isArray(data)) {
                    return {
                        results: data.map(item => ({
                            id: item.id,
                            text: `Crédito: ${item.codigo_credito || item.id} (${item.customer_id?.first_name || ''} ${item.customer_id?.last_name || ''}) - Q ${item.Fsaldo_actual || item.saldo || '0.00'}`
                        }))
                    };
                }
                return { results: [] };
            },
            cache: true
        },
        placeholder: 'Buscar crédito anterior vigente...',
        minimumInputLength: 1
    });

    if (idPreload) {
        const option = new Option(textPreload || `Crédito #${idPreload}`, idPreload, true, true);
        selectEl.append(option).trigger('change');
    }
}

$("#btnAgregarCredito").click(function () {
    agregarFilaCredito();
});

$(document).on('click', '.btn-eliminar-item', function () {
    $(this).closest('.row').remove();
});

// ==========================================================================
// ESTADO DE APROBACIÓN: BADGES Y CONDICIÓN PARA GARANTÍAS COMPLETAS
// ==========================================================================
function actualizarEstadoAprobacion() {
    const estado = ($("#estado_aprobacion").val() || "").toUpperCase();
    const pill = $("#status_pill");

    pill.removeClass("status-pendiente status-aceptado status-negado");

    if (estado === "ACEPTADO") {
        pill.addClass("status-aceptado").html('<i class="bi bi-check-circle-fill"></i> ACEPTADO / APROBADO');
        $("#banner_aprobado_garantias").slideDown(300);
        $("#dynamic-guarantee-fields-container").slideDown(300);
        renderDynamicGuaranteeFields();
    } else if (estado === "NEGADO") {
        pill.addClass("status-negado").html('<i class="bi bi-x-circle-fill"></i> NEGADO');
        $("#banner_aprobado_garantias").slideUp(300);
        $("#dynamic-guarantee-fields-container").slideUp(300);
    } else {
        pill.addClass("status-pendiente").html('<i class="bi bi-clock-history"></i> PENDIENTE');
        $("#banner_aprobado_garantias").slideUp(300);
        $("#dynamic-guarantee-fields-container").slideUp(300);
    }

    // Refrescar tarjetas de garantías para actualizar badges de especificaciones pendientes / completadas
    renderGuaranteeList();
    Object.keys(fiadoresGarantiasMap).forEach(filaId => {
        renderDynamicFiadorFields(filaId);
        renderFiadorGuarantees(filaId);
    });
}

$("#estado_aprobacion").on("change", actualizarEstadoAprobacion);

// ==========================================================================
// RENDERIZADO DINÁMICO DE ESPECIFICACIONES (CREADOR SUPERIOR)
// ==========================================================================
export function renderDynamicGuaranteeFields() {
    const tipo = $("#garantia_tipo_input").val();
    const container = document.getElementById('dynamic-guarantee-fields');
    const specNombre = document.getElementById('spec-tipo-nombre');
    if (specNombre) specNombre.textContent = tipo || '';

    if (!container) return;
    container.innerHTML = '';

    const estado = ($("#estado_aprobacion").val() || "").toUpperCase();
    if (estado !== "ACEPTADO") {
        return;
    }

    container.innerHTML = generarHTMLCamposEspecificacion(tipo, 'json_');

    if (tipo === 'FIADOR') {
        $('#json_fiador_quick_select').select2({
            width: '100%',
            ajax: {
                url: urls_p.api_url_cliente,
                dataType: 'json',
                delay: 250,
                data: function (params) { return { term: params.term }; },
                processResults: function (data) {
                    if (Array.isArray(data)) {
                        return {
                            results: data.map(item => ({
                                id: item.id,
                                text: `${item.customer_code} - ${item.first_name} ${item.last_name}`,
                                raw: item
                            }))
                        };
                    }
                    return { results: [] };
                },
                cache: true
            },
            placeholder: 'Buscar cliente para fiador...',
            minimumInputLength: 1
        }).on('select2:select', function (e) {
            const data = e.params.data.raw;
            if (data) {
                $('#json_fiador_codigo').val(data.customer_code || '');
                $('#json_fiador_nombre').val(`${data.first_name || ''} ${data.last_name || ''}`.trim());
                $('#json_fiador_tel').val(data.phone || data.mobile || '');
            }
        });
    }
}

// Generador reusable de campos HTML para Creador y Modal
function generarHTMLCamposEspecificacion(tipo, prefix = 'json_', values = {}) {
    if (tipo === 'DERECHO DE POSESION HIPOTECA') {
        return `
            <div class="col-md-4">
                <label class="form-label-custom">Nombre</label>
                <input type="text" id="${prefix}nombre" class="form-control glass-input" value="${values.Nombre || 'DERECHO DE POSESIÓN HIPOTECA'}">
            </div>
            <div class="col-md-4">
                <label class="form-label-custom">No. Escritura</label>
                <input type="text" id="${prefix}no_escritura" class="form-control glass-input" placeholder="Ej. 142" value="${values.NoEscritura || ''}">
            </div>
            <div class="col-md-4">
                <label class="form-label-custom">Notario</label>
                <input type="text" id="${prefix}notario" class="form-control glass-input" placeholder="Nombre del Notario" value="${values.Notario || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">Área (m²)</label>
                <input type="text" id="${prefix}area" class="form-control glass-input" placeholder="Ej. 250.00" value="${values.Area || ''}">
            </div>
            <div class="col-md-5">
                <label class="form-label-custom">Ubicación</label>
                <input type="text" id="${prefix}ubicacion" class="form-control glass-input" placeholder="Dirección exacta del inmueble" value="${values.Ubicacion || ''}">
            </div>
            <div class="col-md-4">
                <label class="form-label-custom">Titular</label>
                <input type="text" id="${prefix}titular" class="form-control glass-input" placeholder="Nombre completo del titular" value="${values.Titular || ''}">
            </div>
            <div class="col-md-6">
                <label class="form-label-custom">Descripción Detallada</label>
                <input type="text" id="${prefix}descripcion" class="form-control glass-input" placeholder="Medidas, linderos y colindancias..." value="${values.Descripcion || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">Valor Comercial (Q)</label>
                <input type="number" step="0.01" id="${prefix}valor_comercial" class="form-control glass-input" placeholder="0.00" value="${values.Valor_Comercial || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">Estatus</label>
                <input type="text" id="${prefix}estatus" class="form-control glass-input" value="${values.Estatus || 'GRAVAMEN HIPOTECARIO'}">
            </div>
            <div class="col-md-6">
                <label class="form-label-custom">No. Contrato Arrendamiento</label>
                <input type="text" id="${prefix}no_contrato" class="form-control glass-input" placeholder="Opcional" value="${values.NoContrato_de_Arrendamiento || ''}">
            </div>
            <div class="col-md-6">
                <label class="form-label-custom">Avalúo del Bien</label>
                <input type="text" id="${prefix}avaluo" class="form-control glass-input" placeholder="Entidad o perito valuador" value="${values.avaluoBien || ''}">
            </div>
        `;
    } else if (tipo === 'HIPOTECA') {
        return `
            <div class="col-md-3">
                <label class="form-label-custom">No. Escritura</label>
                <input type="text" id="${prefix}no_escritura" class="form-control glass-input" placeholder="Ej. 245" value="${values.noEscritura || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">Notario</label>
                <input type="text" id="${prefix}notario" class="form-control glass-input" placeholder="Nombre del Notario" value="${values.notario || ''}">
            </div>
            <div class="col-md-2">
                <label class="form-label-custom">Finca</label>
                <input type="text" id="${prefix}finca" class="form-control glass-input" placeholder="Finca" value="${values.finca || ''}">
            </div>
            <div class="col-md-2">
                <label class="form-label-custom">Folio</label>
                <input type="text" id="${prefix}folio" class="form-control glass-input" placeholder="Folio" value="${values.folio || ''}">
            </div>
            <div class="col-md-2">
                <label class="form-label-custom">Libro</label>
                <input type="text" id="${prefix}libro" class="form-control glass-input" placeholder="Libro" value="${values.libro || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">Área (m²)</label>
                <input type="text" id="${prefix}area" class="form-control glass-input" placeholder="Ej. 300.00" value="${values.area || ''}">
            </div>
            <div class="col-md-5">
                <label class="form-label-custom">Ubicación</label>
                <input type="text" id="${prefix}ubicacion" class="form-control glass-input" placeholder="Dirección del bien raíz" value="${values.ubicacion || ''}">
            </div>
            <div class="col-md-4">
                <label class="form-label-custom">Titular</label>
                <input type="text" id="${prefix}titular" class="form-control glass-input" placeholder="Nombre completo del titular" value="${values.titular || ''}">
            </div>
            <div class="col-md-6">
                <label class="form-label-custom">Descripción</label>
                <input type="text" id="${prefix}descripcion" class="form-control glass-input" placeholder="Detalles de construcción..." value="${values.descripcion || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">Valor Comercial (Q)</label>
                <input type="number" step="0.01" id="${prefix}valor_comercial" class="form-control glass-input" placeholder="0.00" value="${values.valor_comercial || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">Estatus</label>
                <input type="text" id="${prefix}estatus" class="form-control glass-input" placeholder="Ej. PRIMERA HIPOTECA" value="${values.estatus || 'PRIMERA HIPOTECA'}">
            </div>
            <div class="col-md-6">
                <label class="form-label-custom">No. Contrato Arrendamiento</label>
                <input type="text" id="${prefix}no_contrato" class="form-control glass-input" placeholder="Opcional" value="${values.noContratoArrendamiento || ''}">
            </div>
            <div class="col-md-6">
                <label class="form-label-custom">Avalúo Bien</label>
                <input type="text" id="${prefix}avaluo" class="form-control glass-input" placeholder="Valuador registrado" value="${values.avaluoBien || ''}">
            </div>
        `;
    } else if (tipo === 'FIADOR') {
        return `
            <div class="col-md-6">
                <label class="form-label-custom">Código de Cliente Fiador</label>
                <input type="text" id="${prefix}fiador_codigo" class="form-control glass-input" placeholder="Código de cliente" value="${values.Codigo_de_Cliente || ''}">
            </div>
            <div class="col-md-6">
                <label class="form-label-custom">Nombre Completo Fiador</label>
                <input type="text" id="${prefix}fiador_nombre" class="form-control glass-input" placeholder="Nombres y Apellidos" value="${values.Nombre || ''}">
            </div>
            <div class="col-md-6">
                <label class="form-label-custom">Lugar de Trabajo</label>
                <input type="text" id="${prefix}fiador_trabajo" class="form-control glass-input" placeholder="Empresa o institución" value="${values.Lugar_de_Trabajo || ''}">
            </div>
            <div class="col-md-6">
                <label class="form-label-custom">Número de Teléfono</label>
                <input type="text" id="${prefix}fiador_tel" class="form-control glass-input" placeholder="Teléfono de contacto" value="${values.Numero_de_Telefono || ''}">
            </div>
            <div class="col-md-6">
                <label class="form-label-custom">Ingresos Mensuales (Q)</label>
                <input type="number" step="0.01" id="${prefix}fiador_ingreso" class="form-control glass-input" placeholder="0.00" value="${values.Ingresos || ''}">
            </div>
        `;
    } else if (tipo === 'CHEQUE / PAGARE') {
        return `
            <div class="col-md-4">
                <label class="form-label-custom">No. de Cheque / Pagaré</label>
                <input type="text" id="${prefix}no_cheque" class="form-control glass-input" placeholder="Ej. 00000388" value="${values.noCheque || ''}">
            </div>
            <div class="col-md-4">
                <label class="form-label-custom">No. de Cuenta</label>
                <input type="text" id="${prefix}no_cuenta" class="form-control glass-input" placeholder="Ej. 3197005470" value="${values.noCuenta || ''}">
            </div>
            <div class="col-md-4">
                <label class="form-label-custom">Nombre de la Cuenta</label>
                <input type="text" id="${prefix}nombre_cuenta" class="form-control glass-input" placeholder="Titular de la cuenta" value="${values.NombreCuenta || ''}">
            </div>
            <div class="col-md-4">
                <label class="form-label-custom">Banco Emisor</label>
                <input type="text" id="${prefix}banco" class="form-control glass-input" placeholder="Ej. Banco Industrial, Banrural..." value="${values.Banco || ''}">
            </div>
            <div class="col-md-4">
                <label class="form-label-custom">Cheque Girado A</label>
                <input type="text" id="${prefix}girado_a" class="form-control glass-input" value="${values.Cheque_girado_a || 'INVERSIONES INTEGRALES EL TELAR S.A.'}">
            </div>
            <div class="col-md-4">
                <label class="form-label-custom">Monto del Cheque (Q)</label>
                <input type="number" step="0.01" id="${prefix}monto_cheque" class="form-control glass-input" placeholder="0.00" value="${values.Monto_cheque || ''}">
            </div>
        `;
    } else if (tipo === 'VEHICULO') {
        return `
            <div class="col-md-3">
                <label class="form-label-custom">No. de Placa</label>
                <input type="text" id="${prefix}veh_placa" class="form-control glass-input" placeholder="Ej. P-123XYZ" value="${values.Placa || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">Marca</label>
                <input type="text" id="${prefix}veh_marca" class="form-control glass-input" placeholder="Ej. Toyota, Hilux" value="${values.Marca || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">Color</label>
                <input type="text" id="${prefix}veh_color" class="form-control glass-input" placeholder="Ej. Blanco" value="${values.Color || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">No. Chasis / VIN</label>
                <input type="text" id="${prefix}veh_chasis" class="form-control glass-input" placeholder="Número de chasis" value="${values.NoChasis || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">No. Motor</label>
                <input type="text" id="${prefix}veh_motor" class="form-control glass-input" placeholder="Número de motor" value="${values.NoMotor || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">Valor Comercial (Q)</label>
                <input type="number" step="0.01" id="${prefix}veh_valor" class="form-control glass-input" placeholder="0.00" value="${values.Valor_Comercial || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">Tarjeta de Circulación</label>
                <input type="text" id="${prefix}veh_tarjeta" class="form-control glass-input" placeholder="No. de tarjeta" value="${values.tarjeta_circulacion || ''}">
            </div>
            <div class="col-md-3">
                <label class="form-label-custom">Título de Propiedad</label>
                <input type="text" id="${prefix}veh_titulo" class="form-control glass-input" placeholder="No. de título" value="${values.titulo || ''}">
            </div>
            <div class="col-md-4">
                <label class="form-label-custom">No. Póliza de Seguro</label>
                <input type="text" id="${prefix}veh_poliza" class="form-control glass-input" placeholder="No. Póliza" value="${values.NoPoliza || ''}">
            </div>
            <div class="col-md-4">
                <label class="form-label-custom">Monto Seguro (Q)</label>
                <input type="number" step="0.01" id="${prefix}veh_seguro" class="form-control glass-input" placeholder="0.00" value="${values.MontoSeguro || ''}">
            </div>
            <div class="col-md-4">
                <label class="form-label-custom">Contrato Arrendamiento</label>
                <input type="text" id="${prefix}veh_contrato" class="form-control glass-input" placeholder="Opcional" value="${values.NoContratoArrendamiento || ''}">
            </div>
        `;
    } else if (tipo === 'MOBILIARIA') {
        return `
            <div class="col-md-6">
                <label class="form-label-custom">Descripción Detallada del Bien</label>
                <input type="text" id="${prefix}mob_desc" class="form-control glass-input" placeholder="Marca, modelo, número de serie, maquinaria..." value="${values.DescripcionBien || ''}">
            </div>
            <div class="col-md-6">
                <label class="form-label-custom">Documento que Acredita</label>
                <input type="text" id="${prefix}mob_doc" class="form-control glass-input" placeholder="Factura, contrato de compraventa, póliza..." value="${values.DocumentoAcredita || ''}">
            </div>
            <div class="col-md-6">
                <label class="form-label-custom">No. Póliza de Seguro</label>
                <input type="text" id="${prefix}mob_poliza" class="form-control glass-input" placeholder="Opcional" value="${values.NoPoliza || ''}">
            </div>
            <div class="col-md-6">
                <label class="form-label-custom">Monto Seguro (Q)</label>
                <input type="number" step="0.01" id="${prefix}mob_seguro" class="form-control glass-input" placeholder="0.00" value="${values.MontoSeguro || ''}">
            </div>
        `;
    }
    return '';
}

// Extracción de especificaciones por prefijo
function extraerEspecificacionesGenerico(tipo, prefix = 'json_') {
    let especificaciones = {};

    if (tipo === 'DERECHO DE POSESION HIPOTECA') {
        especificaciones = {
            Nombre: document.getElementById(`${prefix}nombre`)?.value || "DERECHO DE POSESIÓN HIPOTECA",
            NoEscritura: document.getElementById(`${prefix}no_escritura`)?.value || "",
            Notario: document.getElementById(`${prefix}notario`)?.value || "",
            Area: document.getElementById(`${prefix}area`)?.value || "",
            Ubicacion: document.getElementById(`${prefix}ubicacion`)?.value || "",
            Descripcion: document.getElementById(`${prefix}descripcion`)?.value || "",
            Valor_Comercial: parseFloat(document.getElementById(`${prefix}valor_comercial`)?.value) || null,
            Titular: document.getElementById(`${prefix}titular`)?.value || "",
            Estatus: document.getElementById(`${prefix}estatus`)?.value || "GRAVAMEN HIPOTECARIO",
            NoContrato_de_Arrendamiento: document.getElementById(`${prefix}no_contrato`)?.value || "",
            avaluoBien: document.getElementById(`${prefix}avaluo`)?.value || ""
        };
    } else if (tipo === 'HIPOTECA') {
        especificaciones = {
            noEscritura: document.getElementById(`${prefix}no_escritura`)?.value || "",
            notario: document.getElementById(`${prefix}notario`)?.value || "",
            finca: document.getElementById(`${prefix}finca`)?.value || "",
            folio: document.getElementById(`${prefix}folio`)?.value || "",
            libro: document.getElementById(`${prefix}libro`)?.value || "",
            area: document.getElementById(`${prefix}area`)?.value || "",
            ubicacion: document.getElementById(`${prefix}ubicacion`)?.value || "",
            descripcion: document.getElementById(`${prefix}descripcion`)?.value || "",
            valor_comercial: parseFloat(document.getElementById(`${prefix}valor_comercial`)?.value) || null,
            titular: document.getElementById(`${prefix}titular`)?.value || "",
            estatus: document.getElementById(`${prefix}estatus`)?.value || "PRIMERA HIPOTECA",
            noContratoArrendamiento: document.getElementById(`${prefix}no_contrato`)?.value || "",
            avaluoBien: document.getElementById(`${prefix}avaluo`)?.value || ""
        };
    } else if (tipo === 'FIADOR') {
        especificaciones = {
            Codigo_de_Cliente: document.getElementById(`${prefix}fiador_codigo`)?.value || '',
            Nombre: document.getElementById(`${prefix}fiador_nombre`)?.value || '',
            Lugar_de_Trabajo: document.getElementById(`${prefix}fiador_trabajo`)?.value || '',
            Ingresos: parseFloat(document.getElementById(`${prefix}fiador_ingreso`)?.value) || 0,
            Numero_de_Telefono: document.getElementById(`${prefix}fiador_tel`)?.value || ''
        };
    } else if (tipo === 'CHEQUE / PAGARE') {
        especificaciones = {
            noCheque: document.getElementById(`${prefix}no_cheque`)?.value || "",
            noCuenta: document.getElementById(`${prefix}no_cuenta`)?.value || "",
            NombreCuenta: document.getElementById(`${prefix}nombre_cuenta`)?.value || "",
            Banco: document.getElementById(`${prefix}banco`)?.value || "",
            Cheque_girado_a: document.getElementById(`${prefix}girado_a`)?.value || "",
            Monto_cheque: parseFloat(document.getElementById(`${prefix}monto_cheque`)?.value) || 0
        };
    } else if (tipo === 'VEHICULO') {
        especificaciones = {
            Placa: document.getElementById(`${prefix}veh_placa`)?.value || "",
            Marca: document.getElementById(`${prefix}veh_marca`)?.value || "",
            Color: document.getElementById(`${prefix}veh_color`)?.value || "",
            NoChasis: document.getElementById(`${prefix}veh_chasis`)?.value || "",
            NoMotor: document.getElementById(`${prefix}veh_motor`)?.value || "",
            Valor_Comercial: parseFloat(document.getElementById(`${prefix}veh_valor`)?.value) || null,
            tarjeta_circulacion: document.getElementById(`${prefix}veh_tarjeta`)?.value || "",
            titulo: document.getElementById(`${prefix}veh_titulo`)?.value || "",
            NoPoliza: document.getElementById(`${prefix}veh_poliza`)?.value || "",
            MontoSeguro: parseFloat(document.getElementById(`${prefix}veh_seguro`)?.value) || null,
            NoContratoArrendamiento: document.getElementById(`${prefix}veh_contrato`)?.value || ""
        };
    } else if (tipo === 'MOBILIARIA') {
        especificaciones = {
            DescripcionBien: document.getElementById(`${prefix}mob_desc`)?.value || "",
            DocumentoAcredita: document.getElementById(`${prefix}mob_doc`)?.value || "",
            NoPoliza: document.getElementById(`${prefix}mob_poliza`)?.value || "",
            MontoSeguro: parseFloat(document.getElementById(`${prefix}mob_seguro`)?.value) || null
        };
    }

    return especificaciones;
}

// Control del Notario en el Creador de Garantía (regla CHEQUE / PAGARE > 500)
function evaluarNotarioBuilder() {
    const tipo = $("#garantia_tipo_input").val();
    const valor = parseFloat($("#garantia_valor_input").val()) || 0;
    const contenedor = $("#contenedor_notario_builder");

    if (tipo === "CHEQUE / PAGARE" && valor > 500) {
        contenedor.fadeIn(200);
    } else {
        contenedor.fadeOut(200);
        $("#garantia_notario_builder").val(null).trigger('change');
    }
}

$("#garantia_tipo_input").on("change", function () {
    renderDynamicGuaranteeFields();
    evaluarNotarioBuilder();
});

$("#garantia_valor_input").on("keyup change", function () {
    evaluarNotarioBuilder();
});

// ==========================================================================
// MONITOR DE COBERTURA EN TIEMPO REAL
// ==========================================================================
function formatearMonedaQ(monto) {
    return 'Q ' + (parseFloat(monto) || 0).toLocaleString('es-GT', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

function obtenerGarantiasFiadores() {
    const todas = [];
    $(".fila-fiador").each(function () {
        const filaId = $(this).attr("id");
        const lista = fiadoresGarantiasMap[filaId] || [];
        lista.forEach(g => todas.push(g));
    });
    return todas;
}

function actualizarMonitorCobertura() {
    const montoRequerido = parseFloat($("#total_value_of_the_product_or_service").val()) || 0;
    const totalGarantiasPlan = guaranteeList.reduce((acc, g) => acc + (parseFloat(g.valor) || 0), 0);
    const totalGarantiasFiadores = obtenerGarantiasFiadores().reduce((acc, g) => acc + (parseFloat(g.valor) || 0), 0);
    const totalGarantias = totalGarantiasPlan + totalGarantiasFiadores;

    $("#display-monto-solicitado").text(formatearMonedaQ(montoRequerido));
    $("#registered-guarantee-total").text(formatearMonedaQ(totalGarantias));

    const porcentaje = montoRequerido > 0 ? Math.round((totalGarantias / montoRequerido) * 100) : (totalGarantias > 0 ? 100 : 0);
    $("#coverage-percent").text(porcentaje + '%');

    const progressBar = $("#coverage_progress_bar");
    const statusBadge = $("#coverage-status-badge");

    progressBar.css("width", Math.min(porcentaje, 100) + "%");

    if (totalGarantias >= montoRequerido && montoRequerido > 0) {
        progressBar.removeClass("insufficient").addClass("sufficient");
        statusBadge.removeClass("bg-warning text-dark bg-danger").addClass("bg-success text-white")
            .html(`<i class="bi bi-shield-check"></i> Cobertura Completa (${porcentaje}%)`);
    } else {
        progressBar.removeClass("sufficient").addClass("insufficient");
        statusBadge.removeClass("bg-success text-white").addClass("bg-warning text-dark")
            .html(`<i class="bi bi-exclamation-triangle"></i> Cobertura Pendiente (${porcentaje}%)`);
    }
}

$("#total_value_of_the_product_or_service").on("keyup change", actualizarMonitorCobertura);

// ==========================================================================
// RENDERIZADO DE LA LISTA DE GARANTÍAS REGISTRADAS
// ==========================================================================
function renderGuaranteeList() {
    const container = $("#lista_garantias");
    const countBadge = $("#badge-garantias-count");

    countBadge.text(`${guaranteeList.length} Registrada${guaranteeList.length === 1 ? '' : 's'}`);

    if (guaranteeList.length === 0) {
        container.html(`
            <div class="empty-placeholder" id="empty-garantias-notice">
                <i class="bi bi-shield-slash"></i>
                <p class="fw-bold">No se han registrado garantías todavía.</p>
                <small>Utilice el formulario superior para añadir al menos una garantía que cubra el monto del crédito.</small>
            </div>
        `);
        actualizarMonitorCobertura();
        return;
    }

    container.empty();

    const estadoAprobado = ($("#estado_aprobacion").val() || "").toUpperCase() === "ACEPTADO";

    guaranteeList.forEach((g, index) => {
        const notarioText = (g.notario && g.notario.nombre) ? g.notario.nombre : null;
        const notarioNotifyBadge = (g.notario && g.notario.id)
            ? (g.notario.notificar !== false
                ? `<span class="badge bg-success-subtle text-success border border-success-subtle ms-1"><i class="bi bi-envelope-check"></i> Notificar</span>`
                : `<span class="badge bg-secondary-subtle text-secondary border border-secondary-subtle ms-1"><i class="bi bi-envelope-slash"></i> Sin notificación</span>`)
            : '';
        const specs = g.especificaciones || {};
        const keys = Object.keys(specs);
        const hasSpecs = keys.some(k => specs[k] !== null && specs[k] !== '' && specs[k] !== undefined);

        let statusBadgeSpecsHTML = '';
        if (estadoAprobado) {
            if (hasSpecs) {
                statusBadgeSpecsHTML = `<span class="badge-specs-complete ms-2"><i class="bi bi-check-circle-fill"></i> Especificaciones completadas</span>`;
            } else {
                statusBadgeSpecsHTML = `<span class="badge-specs-pending ms-2"><i class="bi bi-exclamation-triangle-fill"></i> Especificaciones pendientes</span>`;
            }
        }

        let specsBadgesHTML = '';
        if (hasSpecs) {
            specsBadgesHTML = Object.entries(specs)
                .filter(([_, val]) => val !== null && val !== '' && val !== undefined)
                .map(([key, val]) => `
                    <div class="spec-chip">
                        <span class="spec-key">${key.replace(/_/g, ' ')}</span>
                        <span class="spec-val">${val}</span>
                    </div>
                `).join('');
        }

        const cardHTML = $(`
            <div class="guarantee-item-card animate-fade-in" data-index="${index}">
                <div class="d-flex justify-content-between align-items-start gap-2 flex-wrap">
                    <div>
                        <div class="d-flex align-items-center flex-wrap gap-1">
                            <span class="guarantee-tag">
                                <i class="bi bi-shield-shaded me-1"></i> ${g.tipo}
                            </span>
                            ${statusBadgeSpecsHTML}
                        </div>
                        <h6 class="fw-bold text-dark mb-1 mt-1">${g.descripcion || 'Sin descripción'}</h6>
                        <span class="text-xs text-muted">
                            Monto Cobertura: <strong class="text-dark font-monospace">${formatearMonedaQ(g.valor)}</strong>
                            ${notarioText ? `&nbsp;|&nbsp; <span class="badge bg-secondary"><i class="bi bi-person-fill"></i> Notario: ${notarioText}</span>${notarioNotifyBadge}` : ''}
                        </span>
                    </div>

                    <div class="text-end d-flex flex-column align-items-end gap-1">
                        <span class="fs-6 fw-bold text-danger font-monospace d-block">${formatearMonedaQ(g.valor)}</span>
                        <div class="d-flex align-items-center gap-1 mt-1">
                            <button type="button" class="btn btn-sm ${estadoAprobado && !hasSpecs ? 'btn-danger btn-completar-pulsing text-white' : 'btn-outline-primary'} btn-editar-garantia" data-index="${index}" title="Modificar Garantía / Completar Especificaciones">
                                <i class="bi bi-pencil-square"></i> ${estadoAprobado && !hasSpecs ? 'Completar Especificaciones' : 'Modificar'}
                            </button>
                            <button type="button" class="btn btn-sm btn-outline-danger btn-remover-garantia" data-index="${index}" title="Quitar Garantía">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>

                ${hasSpecs && specsBadgesHTML ? `
                    <div class="mt-2">
                        <a href="javascript:void(0);" class="btn-toggle-specs small text-primary text-decoration-none fw-bold" style="font-size: 0.775rem;">
                            <i class="bi bi-chevron-down"></i> Ver Especificaciones Técnicas (${Object.keys(specs).length} campos)
                        </a>
                        <div class="specs-detail-grid mt-2" style="display: none;">
                            ${specsBadgesHTML}
                        </div>
                    </div>
                ` : ''}
            </div>
        `);

        container.append(cardHTML);
    });

    actualizarMonitorCobertura();
}

// Toggle para ver/ocultar especificaciones en la tarjeta de garantía
$(document).on('click', '.btn-toggle-specs', function(e) {
    e.preventDefault();
    const specsContainer = $(this).siblings('.specs-detail-grid');
    specsContainer.slideToggle(200);
    $(this).find('i').toggleClass('bi-chevron-down bi-chevron-up');
});

// Remover garantía del arreglo
$(document).on('click', '.btn-remover-garantia', function() {
    const index = parseInt($(this).data('index'));
    if (!isNaN(index) && index >= 0 && index < guaranteeList.length) {
        guaranteeList.splice(index, 1);
        renderGuaranteeList();
        showToast('Garantía eliminada de la lista.', 'info');
    }
});

// ==========================================================================
// MODAL DE MODIFICACIÓN Y COMPLETADO DE GARANTÍA (SIN VOLVER A REGISTRAR)
// ==========================================================================
function evaluarNotarioModal() {
    const tipo = $("#modal_garantia_tipo").val();
    const valor = parseFloat($("#modal_garantia_valor").val()) || 0;
    const contenedor = $("#modal_contenedor_notario");

    if (tipo === "CHEQUE / PAGARE" && valor > 500) {
        contenedor.fadeIn(200);
    } else {
        contenedor.fadeOut(200);
        $("#modal_garantia_notario").val(null).trigger('change');
    }
}

$("#modal_garantia_tipo").on("change", function () {
    const tipo = $(this).val();
    $("#modal_spec_tipo_nombre").text(tipo);
    const index = parseInt($("#modal_edit_index").val());
    const fiadorFilaId = $("#modal_edit_fiador_id").val() || "";
    const targetList = fiadorFilaId ? (fiadoresGarantiasMap[fiadorFilaId] || []) : guaranteeList;
    const existingSpecs = (!isNaN(index) && targetList[index] && targetList[index].tipo === tipo) ? targetList[index].especificaciones : {};
    
    $("#modal_dynamic_fields").html(generarHTMLCamposEspecificacion(tipo, 'modal_json_', existingSpecs));
    evaluarNotarioModal();
});

$("#modal_garantia_valor").on("keyup change", function () {
    evaluarNotarioModal();
});

function abrirModalEdicionGarantia(index, fiadorFilaId = null) {
    const targetList = fiadorFilaId ? (fiadoresGarantiasMap[fiadorFilaId] || []) : guaranteeList;
    if (isNaN(index) || index < 0 || index >= targetList.length) {
        return;
    }

    const g = targetList[index];
    $("#modal_edit_index").val(index);
    $("#modal_edit_fiador_id").val(fiadorFilaId || "");
    $("#modal_garantia_tipo").val(g.tipo);
    $("#modal_spec_tipo_nombre").text(g.tipo);
    $("#modal_garantia_desc").val(g.descripcion || "");
    $("#modal_garantia_valor").val(g.valor || "");

    // Cargar campos dinámicos con los valores existentes
    $("#modal_dynamic_fields").html(generarHTMLCamposEspecificacion(g.tipo, 'modal_json_', g.especificaciones || {}));

    // Cargar notario si aplica
    if (g.tipo === "CHEQUE / PAGARE" && parseFloat(g.valor) > 500) {
        $("#modal_contenedor_notario").show();
        if (g.notario && g.notario.id) {
            const option = new Option(g.notario.nombre, g.notario.id, true, true);
            $("#modal_garantia_notario").empty().append(option).trigger('change');
            $("#modal_notificar_notario").prop('checked', g.notario.notificar !== false);
            $("#modal_contenedor_notificar_notario").show();
        } else {
            $("#modal_garantia_notario").val(null).trigger('change');
            $("#modal_notificar_notario").prop('checked', true);
            $("#modal_contenedor_notificar_notario").hide();
        }
    } else {
        $("#modal_contenedor_notario").hide();
        $("#modal_garantia_notario").val(null).trigger('change');
        $("#modal_notificar_notario").prop('checked', true);
        $("#modal_contenedor_notificar_notario").hide();
    }

    // Abrir Modal Bootstrap
    const modalEl = document.getElementById('modalEditarGarantia');
    if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
        const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
        modal.show();
    } else {
        $(modalEl).modal('show');
    }
}

$(document).on('click', '.btn-editar-garantia', function () {
    const index = parseInt($(this).data('index'));
    abrirModalEdicionGarantia(index, null);
});

// Guardar los cambios hechos en el Modal
$("#btnGuardarEdicionGarantia").click(function () {
    const index = parseInt($("#modal_edit_index").val());
    const fiadorFilaId = $("#modal_edit_fiador_id").val() || "";
    const targetList = fiadorFilaId ? (fiadoresGarantiasMap[fiadorFilaId] || []) : guaranteeList;

    if (isNaN(index) || index < 0 || index >= targetList.length) {
        return;
    }

    const tipo = $("#modal_garantia_tipo").val();
    const descripcion = ($("#modal_garantia_desc").val() || "").trim();
    const valor = parseFloat($("#modal_garantia_valor").val()) || 0;

    if (!tipo) {
        Swal.fire('Atención', 'Seleccione el tipo de garantía.', 'warning');
        return;
    }

    if (!descripcion) {
        Swal.fire('Atención', 'Ingrese la descripción de la garantía.', 'warning');
        $("#modal_garantia_desc").focus();
        return;
    }

    if (valor <= 0) {
        Swal.fire('Atención', 'Ingrese un valor de cobertura válido superior a Q 0.00.', 'warning');
        $("#modal_garantia_valor").focus();
        return;
    }

    // Capturar Notario de garantía si aplica
    let notarioGarantia = null;
    const notarioSelect = $("#modal_garantia_notario");
    if (tipo === "CHEQUE / PAGARE" && valor > 500 && notarioSelect.val()) {
        notarioGarantia = {
            id: parseInt(notarioSelect.val()),
            nombre: notarioSelect.find('option:selected').text(),
            notificar: $("#modal_notificar_notario").is(":checked")
        };
    }

    // Capturar especificaciones desde el modal
    const especificaciones = extraerEspecificacionesGenerico(tipo, 'modal_json_');

    // Actualizar elemento en la lista correspondiente preservando ID
    targetList[index] = {
        ...targetList[index],
        tipo: tipo,
        descripcion: descripcion,
        valor: valor,
        notario: notarioGarantia,
        especificaciones: especificaciones
    };

    // Cerrar Modal Bootstrap
    const modalEl = document.getElementById('modalEditarGarantia');
    if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
        const modalInstance = bootstrap.Modal.getInstance(modalEl);
        if (modalInstance) modalInstance.hide();
    } else {
        $(modalEl).modal('hide');
    }

    if (fiadorFilaId) {
        renderFiadorGuarantees(fiadorFilaId);
        actualizarMonitorCobertura();
    } else {
        renderGuaranteeList();
    }
    showToast('Garantía modificada y especificaciones guardadas exitosamente.', 'success');
});

// ==========================================================================
// REGISTRAR NUEVA GARANTÍA DESDE EL BUILDER
// ==========================================================================
$("#btnAgregarGarantia").click(function () {
    const tipo = $("#garantia_tipo_input").val();
    const descripcion = ($("#garantia_desc_input").val() || "").trim();
    const valor = parseFloat($("#garantia_valor_input").val()) || 0;
    const estado = ($("#estado_aprobacion").val() || "").toUpperCase();

    if (!tipo) {
        Swal.fire('Atención', 'Seleccione el tipo de garantía.', 'warning');
        return;
    }

    if (!descripcion) {
        Swal.fire('Atención', 'Ingrese la descripción o resumen de la garantía.', 'warning');
        $("#garantia_desc_input").focus();
        return;
    }

    if (valor <= 0) {
        Swal.fire('Atención', 'Ingrese un valor de cobertura válido superior a Q 0.00.', 'warning');
        $("#garantia_valor_input").focus();
        return;
    }

    // Capturar Notario de garantía si aplica
    let notarioGarantia = null;
    const notarioSelect = $("#garantia_notario_builder");
    if (tipo === "CHEQUE / PAGARE" && valor > 500 && notarioSelect.val()) {
        notarioGarantia = {
            id: parseInt(notarioSelect.val()),
            nombre: notarioSelect.find('option:selected').text(),
            notificar: $("#notificar_notario_garantia").is(":checked")
        };
    }

    // Capturar especificaciones dinámicas si está aprobado
    let especificaciones = {};
    if (estado === "ACEPTADO") {
        especificaciones = extraerEspecificacionesGenerico(tipo, 'json_');
    }

    const nuevaGarantia = {
        id: Date.now() + Math.floor(Math.random() * 100),
        tipo: tipo,
        descripcion: descripcion,
        valor: valor,
        notario: notarioGarantia,
        especificaciones: especificaciones
    };

    guaranteeList.push(nuevaGarantia);

    // Resetear inputs del creador
    $("#garantia_desc_input").val('');
    $("#garantia_valor_input").val('');
    $("#notificar_notario_garantia").prop('checked', true);
    renderDynamicGuaranteeFields();
    evaluarNotarioBuilder();

    renderGuaranteeList();
    showToast('Garantía agregada exitosamente.', 'success');
});

// ==========================================================================
// VALIDACIONES GENERALES DEL FORMULARIO
// ==========================================================================
function validarFormulario() {
    if (!$("#asesor_responsable").val()) {
        Swal.fire('Campo requerido', 'Debe seleccionar un asesor responsable.', 'warning');
        return false;
    }

    if (!$("#type_of_product_or_service").val()) {
        Swal.fire('Campo requerido', 'Debe seleccionar el tipo de producto.', 'warning');
        return false;
    }

    if (!$("#forma_de_pago").val()) {
        Swal.fire('Campo requerido', 'Debe seleccionar la forma de pago.', 'warning');
        return false;
    }

    const valorTotalProducto = parseFloat($("#total_value_of_the_product_or_service").val()) || 0;
    if (valorTotalProducto <= 0) {
        Swal.fire('Campo requerido', 'Debe ingresar un valor del producto (monto solicitado) mayor a cero.', 'warning');
        return false;
    }

    if (!$("#tasa_interes").val()) {
        Swal.fire('Campo requerido', 'Debe ingresar la tasa de interés.', 'warning');
        return false;
    }

    if (!$("#fecha_inicio").val()) {
        Swal.fire('Campo requerido', 'Debe seleccionar la fecha de inicio.', 'warning');
        return false;
    }

    if (!$("#plazo").val() || parseInt($("#plazo").val()) <= 0) {
        Swal.fire('Campo requerido', 'Debe ingresar el plazo en meses.', 'warning');
        return false;
    }

    if (!$("#tipo_documento").val()) {
        Swal.fire('Campo requerido', 'Debe seleccionar el tipo de documento legal.', 'warning');
        return false;
    }

    const formaPagoVal = $("#forma_de_pago").val();
    const plazoGarantia = $("#plazo_garantia").val();
    if ((formaPagoVal === "INTERES MENSUAL Y CAPITAL AL VENCIMIENTO" || formaPagoVal === "INTERES Y CAPITAL AL VENCIMIENTO") && !plazoGarantia) {
        Swal.fire('Campo requerido', 'Debe ingresar el plazo de gracia/garantía para esta forma de pago.', 'warning');
        return false;
    }

    const tipoDocVal = $("#tipo_documento").val();
    const claseDocVal = ($("#clase_de_documento").val() || "").trim().toUpperCase();

    if (tipoDocVal === "RECONOCIMIENTO DE DEUDA") {
        if (!claseDocVal) {
            Swal.fire('Campo requerido', 'Debe seleccionar la clase de documento (Individual, Fiduciario o Mobiliario) para el Reconocimiento de Deuda.', 'warning');
            return false;
        }
    }

    if (tipoDocVal === "PAGARE") {
        const tipoPag = $("#tipo_pagare").val();
        if (!tipoPag) {
            Swal.fire('Campo requerido', 'Debe seleccionar la modalidad de pagaré.', 'warning');
            return false;
        }

        if (tipoPag === "Fiador" && $(".fiador_select").length === 0) {
            Swal.fire('Campo requerido', 'Debe agregar al menos un fiador para el pagaré con fiador.', 'warning');
            return false;
        }

        if (tipoPag === "Restructuracion" && $(".credito_vigente").length === 0) {
            Swal.fire('Campo requerido', 'Debe agregar al menos un crédito anterior vigente para restructuración.', 'warning');
            return false;
        }
    }

    // Validar que todos los fiadores agregados tengan cliente seleccionado
    let fiadorVacio = false;
    let fiadorSinGarantiaMarcada = false;
    $(".fila-fiador").each(function () {
        const filaId = $(this).attr("id");
        const val = $(this).find(".fiador_select").val();
        if (!val) {
            fiadorVacio = true;
        } else if ($(this).find(".toggle-fiador-garantia").is(":checked")) {
            const listaF = fiadoresGarantiasMap[filaId] || [];
            if (listaF.length === 0) {
                fiadorSinGarantiaMarcada = true;
            }
        }
    });
    if (fiadorVacio) {
        Swal.fire('Campo requerido', 'Todos los fiadores agregados deben tener un cliente seleccionado.', 'warning');
        return false;
    }
    if (fiadorSinGarantiaMarcada) {
        Swal.fire('Garantía del Fiador', 'Marcó que un fiador deja garantía, pero no ha agregado ninguna garantía en su sección. Agregue al menos una garantía o desactive la opción.', 'warning');
        return false;
    }

    let creditoVacio = false;
    $(".credito_vigente").each(function () {
        if (!$(this).val()) creditoVacio = true;
    });
    if (creditoVacio) {
        Swal.fire('Campo requerido', 'Todos los créditos vigentes agregados deben estar seleccionados.', 'warning');
        return false;
    }

    // Validación de Garantías (Plan + Fiadores)
    const garantiasFiadores = obtenerGarantiasFiadores();
    const todasLasGarantias = [...guaranteeList, ...garantiasFiadores];

    // Reglas específicas según Clase de Documento en Reconocimiento de Deuda
    if (tipoDocVal === "RECONOCIMIENTO DE DEUDA") {
        if (claseDocVal === "FIDUCIARIO" || claseDocVal === "FIDUCIARIA") {
            let cantidadFiadores = 0;
            $(".fila-fiador .fiador_select").each(function () {
                if ($(this).val()) cantidadFiadores++;
            });
            if (cantidadFiadores === 0) {
                Swal.fire(
                    'Fiador Requerido',
                    'Para un Reconocimiento de Deuda de clase Fiduciario debe registrar al menos un fiador.',
                    'warning'
                );
                return false;
            }
        }

        if (claseDocVal === "MOBILIARIO" || claseDocVal === "MOBILIARIA") {
            const tieneGarantiaMobiliaria = todasLasGarantias.some(
                g => (g.tipo || "").trim().toUpperCase() === "MOBILIARIA"
            );
            if (!tieneGarantiaMobiliaria) {
                Swal.fire(
                    'Garantía Mobiliaria Requerida',
                    'Para un Reconocimiento de Deuda de clase Mobiliario debe registrar al menos una garantía de tipo MOBILIARIA (ya sea en el deudor o en algún fiador).',
                    'warning'
                );
                return false;
            }
        }
    }

    if (todasLasGarantias.length === 0) {
        Swal.fire('Garantías requeridas', 'Debe registrar al menos una garantía para la solicitud de financiamiento.', 'warning');
        return false;
    }

    const sumaGarantias = todasLasGarantias.reduce((acc, g) => acc + (parseFloat(g.valor) || 0), 0);
    if (sumaGarantias < valorTotalProducto) {
        Swal.fire({
            icon: "error",
            title: "Garantías Insuficientes",
            text: `La cobertura de las garantías (${formatearMonedaQ(sumaGarantias)}) debe ser mayor o igual al valor del financiamiento (${formatearMonedaQ(valorTotalProducto)}).`
        });
        return false;
    }

    // Validación de Especificaciones cuando el Estado es ACEPTADO
    const estadoAprobacion = ($("#estado_aprobacion").val() || "").toUpperCase();
    if (estadoAprobacion === "ACEPTADO") {
        let garantiasIncompletas = [];
        guaranteeList.forEach((g) => {
            const specs = g.especificaciones || {};
            const values = Object.values(specs).filter(v => v !== null && v !== '' && v !== undefined);
            if (values.length === 0) {
                garantiasIncompletas.push(`• ${g.tipo}: ${g.descripcion || 'Sin descripción'}`);
            }
        });
        garantiasFiadores.forEach((g) => {
            const specs = g.especificaciones || {};
            const values = Object.values(specs).filter(v => v !== null && v !== '' && v !== undefined);
            if (values.length === 0) {
                garantiasIncompletas.push(`• [Fiador] ${g.tipo}: ${g.descripcion || 'Sin descripción'}`);
            }
        });

        if (garantiasIncompletas.length > 0) {
            Swal.fire({
                icon: "warning",
                title: "Especificaciones Incompletas",
                html: `Para aprobar la solicitud, debe completar las especificaciones técnicas y legales de todas las garantías registradas.<br><br>Garantías pendientes:<br><b>${garantiasIncompletas.join('<br>')}</b><br><br>Haga clic en el botón <b>Completar Especificaciones</b> en cada tarjeta de garantía para llenarlas directamente.`
            });
            return false;
        }
    }

    // Validación de Políticas de Riesgo (>= Q25,000)
    if (valorTotalProducto >= 25000) {
        if (!$("#riesgo_comercial").val().trim()) {
            Swal.fire('Políticas de Crédito', 'Para financiamientos iguales o mayores a Q 25,000.00 debe describir los riesgos comerciales principales.', 'warning');
            return false;
        }
        if (!$("#diganostico_oportunidad").val().trim()) {
            Swal.fire('Políticas de Crédito', 'Debe completar el diagnóstico de oportunidades.', 'warning');
            return false;
        }
        if (!$("#mitigadores").val().trim()) {
            Swal.fire('Políticas de Crédito', 'Debe ingresar los mitigadores de riesgo.', 'warning');
            return false;
        }
        if (!$("#evaluacion_mercado").val().trim()) {
            Swal.fire('Políticas de Crédito', 'Debe ingresar la evaluación de mercado.', 'warning');
            return false;
        }
    }

    return true;
}

// ==========================================================================
// ENVÍO DEL FORMULARIO PRINCIPAL
// ==========================================================================
$("#frmInvestmentPlan").on("submit", async function (e) {
    e.preventDefault();

    if (!validarFormulario()) {
        return;
    }

    const estadoAprobacion = ($("#estado_aprobacion").val() || "").toUpperCase();

    // Verificación de código de seguridad cuando se aprueba
    if (estadoAprobacion === "ACEPTADO") {
        const codigoValido = await verificarCodigoSeguridad();
        if (!codigoValido) {
            return;
        }
    }

    const planId = $("#investment_plan_id").val() || null;
    const montoInicial = $("#total_value_of_the_product_or_service").val() ? parseFloat($("#total_value_of_the_product_or_service").val()) : 0.00;
    const tipoDocumentoVal = $("#tipo_documento").val() || null;

    // Recolectar Notarios
    const listaNotariosPayload = [];
    if (tipoDocumentoVal && tipoDocumentoVal !== "PAGARE" && $("#notario_documentacion").val()) {
        listaNotariosPayload.push({
            id: parseInt($("#notario_documentacion").val()),
            nombre: $("#notario_documentacion").find('option:selected').text(),
            modulo: 'documentacion',
            notificar: $("#notificar_notario_doc").is(":checked")
        });
    }

    // Recolectar Notarios desde las garantías registradas
    guaranteeList.forEach(g => {
        if (g.notario && g.notario.id) {
            listaNotariosPayload.push({
                id: g.notario.id,
                nombre: g.notario.nombre,
                modulo: 'garantia',
                notificar: g.notario.notificar !== false
            });
        }
    });

    // Fiadores con sus garantías: [ { id: 2, garantias: [ ... ] } ]
    const fiadores = [];
    $(".fila-fiador").each(function () {
        const filaId = $(this).attr("id");
        const fiadorId = $(this).find(".fiador_select").val();
        if (fiadorId) {
            const garantiasFiador = (fiadoresGarantiasMap[filaId] || []).map(g => {
                if (g.notario && g.notario.id) {
                    listaNotariosPayload.push({
                        id: g.notario.id,
                        nombre: g.notario.nombre,
                        modulo: 'garantia_fiador',
                        notificar: g.notario.notificar !== false
                    });
                }
                return {
                    tipo: g.tipo,
                    descripcion: g.descripcion,
                    valor: g.valor,
                    notario: g.notario || null,
                    especificaciones: g.especificaciones || {}
                };
            });
            fiadores.push({
                id: parseInt(fiadorId),
                garantias: garantiasFiador
            });
        }
    });

    // Créditos Anteriores
    const creditos = [];
    $(".credito_vigente").each(function () {
        if ($(this).val()) {
            creditos.push({ id: parseInt($(this).val()) });
        }
    });

    const payload = {
        customer_id: parseInt($("#customer_id").val()),
        sucursal: parseInt($("#sucursal").val()),
        type_of_product_or_service: $("#type_of_product_or_service").val(),
        total_value_of_the_product_or_service: montoInicial,
        initial_amount: montoInicial,
        monthly_amount: montoInicial,
        sub_destino: $("#sub_destino").val() || null,
        fecha_inicio: $("#fecha_inicio").val() || null,
        plazo: $("#plazo").val() ? parseInt($("#plazo").val()) : null,
        plazo_gracia: $("#plazo_garantia").val() ? parseInt($("#plazo_garantia").val()) : null,
        forma_de_pago: $("#forma_de_pago").val(),
        transfers_or_transfer_of_funds: true,
        type_of_transfers_or_transfer_of_funds: "Local",
        tasa_interes: $("#tasa_interes").val() ? parseFloat($("#tasa_interes").val()) : null,
        tipo_documento: tipoDocumentoVal,
        clase_de_documento: tipoDocumentoVal === "RECONOCIMIENTO DE DEUDA" ? ($("#clase_de_documento").val() || null) : null,
        tipo_pagare: tipoDocumentoVal === "PAGARE" ? ($("#tipo_pagare").val() || null) : null,
        investment_plan_description: $("#investment_plan_description").val() || "",
        riesgo_comercial: $("#riesgo_comercial").val() || "",
        diganostico_oportunidad: $("#diganostico_oportunidad").val() || "",
        mitigadores: $("#mitigadores").val() || "",
        evaluacion_mercado: $("#evaluacion_mercado").val() || "",
        fiador: fiadores,
        credito_anterior_vigente: creditos,
        garantias: guaranteeList.map(g => ({
            tipo: g.tipo,
            descripcion: g.descripcion,
            valor: g.valor,
            notario: g.notario || null,
            especificaciones: g.especificaciones || {}
        })),
        asesor_responsable: parseInt($("#asesor_responsable").val()),
        estado_aprobacion: $("#estado_aprobacion").val(),
        notarios: listaNotariosPayload
    };

    console.log("Enviando Solicitud Plan de Inversión:", payload);

    try {
        const resultado = await savePlanInversion(payload, planId);
        const codigo_cliente = resultado?.id || resultado?.data?.id || planId;

        Swal.fire({
            icon: "success",
            title: "Solicitud Guardada",
            text: "El plan de inversión ha sido guardado exitosamente.",
            timer: 1600,
            showConfirmButton: false,
        });

        setTimeout(() => {
            if (codigo_cliente) {
                window.location.href = `/plan_inversion/gestion_de_expedientes_notarios/${codigo_cliente}/`;
            } else {
                window.location.reload();
            }
        }, 1200);

    } catch (err) {
        let mensajeError = err.response?.data?.message || err.message || "No se pudo procesar la solicitud.";
        const errData = err.response?.data;
        if (errData && typeof errData === "object" && !errData.message) {
            const firstKey = Object.keys(errData)[0];
            if (firstKey) {
                const val = errData[firstKey];
                mensajeError = Array.isArray(val) ? val[0] : String(val);
            }
        }
        Swal.fire({
            icon: "error",
            title: "Error al Guardar",
            text: mensajeError
        });
        console.error("Error al guardar solicitud:", err);
    }
});

// ==========================================================================
// PRE-CARGA DE DATOS EN MODO EDICIÓN
// ==========================================================================
$(document).ready(function () {
    // 1. Visibilidad inicial
    actualizarVisibilidadDocumento();
    actualizarEstadoAprobacion();
    actualizarMonitorCobertura();

    // 2. Comprobar si existe script de datos de precarga
    const preloadEl = document.getElementById("plan-preload-data");
    if (preloadEl) {
        try {
            const planData = JSON.parse(preloadEl.textContent || "{}");

            // Cargar Fiadores (con sus garantías si existen)
            if (Array.isArray(planData.fiadores)) {
                planData.fiadores.forEach(f => {
                    agregarFilaFiador(
                        f.id,
                        f.nombre || `Cliente #${f.id}`,
                        Array.isArray(f.garantias) ? f.garantias : []
                    );
                });
            }

            // Cargar Créditos Anteriores
            if (Array.isArray(planData.creditos)) {
                planData.creditos.forEach(c => {
                    agregarFilaCredito(c.id, c.codigo_credito || `Crédito #${c.id}`);
                });
            }

            // Cargar Garantías Existentes
            if (Array.isArray(planData.garantias)) {
                planData.garantias.forEach(g => {
                    guaranteeList.push({
                        id: Date.now() + Math.floor(Math.random() * 1000),
                        tipo: g.tipo,
                        descripcion: g.descripcion,
                        valor: parseFloat(g.valor) || 0,
                        notario: g.notario || null,
                        especificaciones: g.especificaciones || {}
                    });
                });
                renderGuaranteeList();
            }

            // Cargar Notario de Documentación Global
            if (Array.isArray(planData.notarios)) {
                planData.notarios.forEach(n => {
                    if (n.modulo === 'documentacion' && n.id) {
                        const optionDoc = new Option(n.nombre || `Notario #${n.id}`, n.id, true, true);
                        $("#notario_documentacion").append(optionDoc).trigger('change');
                        $("#notificar_notario_doc").prop('checked', n.notificar !== false);
                        $("#contenedor_notificar_notario_doc").show();
                    }
                });
            }

            // Sincronizar selectores
            setTimeout(() => {
                $('#tipo_documento').trigger('change');
                if (planData.clase_de_documento) {
                    $('#clase_de_documento').val(planData.clase_de_documento.toUpperCase());
                }
                $('#tipo_pagare').trigger('change');
                $('#estado_aprobacion').trigger('change');
                $('#total_value_of_the_product_or_service').trigger('change');
            }, 150);

        } catch (e) {
            console.error("Error al procesar datos de precarga del plan:", e);
        }
    }
});
