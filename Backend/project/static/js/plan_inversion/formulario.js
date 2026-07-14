const tipoDocumento = document.getElementById("tipo_documento");
const tipoPagare = document.getElementById("tipo_pagare");
const contenedorPagare = document.getElementById("contenedor_pagare");
const contenedorFiadores = document.getElementById("contenedor_fiadores");
const contenedorCreditos = document.getElementById("contenedor_creditos");
const contenedorNotariosDoc = document.getElementById("contenedor_notarios_doc");
const notarioDocSelect = $("#notario_documentacion");

import { urls_p } from '../API/urls_api.js'
const URL = urls_p.api_url_investment_plan;


async function verificarCodigoSeguridad() {
    const result = await Swal.fire({
        title: 'Autorización Requerida',
        text: "Ingrese el código de seguridad enviado al administrador:",
        input: 'password',
        inputAttributes: {
            autocapitalize: 'off',
            autocorrect: 'off'
        },
        showCancelButton: true,
        confirmButtonText: 'Verificar y Guardar',
        confirmButtonColor: '#28a745',
        cancelButtonText: 'Cancelar',
        showLoaderOnConfirm: true,
        preConfirm: async (codigoIngresado) => {
            try {
                // Obtener el token CSRF para la petición POST de verificación
                const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
                const csrfToken = csrfTokenElement ? csrfTokenElement.getAttribute('content') : '';

                const response = await fetch('/financings/validar-codigo-seguridad/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken // Añadido soporte CSRF por si lo requiere tu Django
                    },
                    body: JSON.stringify({ codigo: codigoIngresado })
                });

                if (!response.ok) {
                    throw new Error('Error en la red o servidor');
                }
                return await response.json();
            } catch (error) {
                Swal.showValidationMessage(`Solicitud fallida: ${error.message}`);
            }
        },
        allowOutsideClick: () => !Swal.isLoading()
    });

    if (result.isConfirmed) {
        if (result.value && result.value.valido) {
            Swal.fire({
                title: '¡Éxito!',
                text: 'Código verificado correctamente.',
                icon: 'success',
                timer: 1500,
                showConfirmButton: false
            });
            // Esperamos un segundo para que el usuario aprecie el feedback visual
            await new Promise(resolve => setTimeout(resolve, 1000));
            return true;
        } else {
            Swal.fire('Error', 'El código ingresado es incorrecto.', 'error');
            return false;
        }
    }
    return false; // El usuario canceló la alerta
}

// Inicializar Select2 para el notario de documentación
notarioDocSelect.select2({
    width: '100%',
    ajax: {
        url: urls_p.api_url_notario, // Ajusta a tu endpoint real de notarios
        dataType: 'json',
        delay: 250,
        data: function (params) { return { term: params.term }; },
        processResults: function (data) {
            return {
                results: data.map(item => ({ id: item.id, text: item.nombre_completo || item.nombre }))
            };
        },
        cache: true
    },
    placeholder: 'Seleccione al Notario',
    allowClear: true
});




export async function savePlanInversion(formData, planId = null) {
    try {
        const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
        if (!csrfTokenElement) throw new Error('CSRF token not found');
        const csrfToken = csrfTokenElement.getAttribute('content');

        // Si hay un planId, apuntamos a la URL de detalle (ej: /api/investment-plan/5/), sino a la lista general
        const urlFinal = planId ? `${urls_p.api_url_investment_plan}${planId}/` : urls_p.api_url_investment_plan;
        const metodo = planId ? 'put' : 'post'; // O 'patch' si solo actualizas parcialmente

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

contenedorPagare.style.display = "none";
contenedorFiadores.style.display = "none";
contenedorCreditos.style.display = "none";

const formaPago = document.getElementById("forma_de_pago");
const contenedorPlazoGarantia = document.getElementById("contenedor_plazo_garantia");

formaPago.addEventListener("change", () => {
    const valorSeleccionado = formaPago.value;

    if (valorSeleccionado === "INTERES MENSUAL Y CAPITAL AL VENCIMIENTO" || 
        valorSeleccionado === "INTERES Y CAPITAL AL VENCIMIENTO") {
        $(contenedorPlazoGarantia).fadeIn();
    } else {
        $(contenedorPlazoGarantia).fadeOut();
        document.getElementById("plazo_garantia").value = "";
    }
});

tipoDocumento.addEventListener("change", () => {
    contenedorPagare.style.display = "none";
    contenedorFiadores.style.display = "none";
    contenedorCreditos.style.display = "none";

    if (tipoDocumento.value == "PAGARE") {
        contenedorPagare.style.display = "block";
    }
});

tipoPagare.addEventListener("change", () => {
    contenedorFiadores.style.display = "none";
    contenedorCreditos.style.display = "none";

    if (tipoPagare.value == "FIADOR" || tipoPagare.value == "Fiador") {
        contenedorFiadores.style.display = "block";
    }

    if (tipoPagare.value == "REESTRUCTURACION" || tipoPagare.value == "Restructuracion") {
        contenedorCreditos.style.display = "block";
    }
});

// --- LÓGICA DE VISIBILIDAD DE CONTENEDORES ---

function actualizarVisibilidadDocumento() {
    contenedorPagare.style.display = "none";
    contenedorFiadores.style.display = "none";
    contenedorCreditos.style.display = "none";
    contenedorNotariosDoc.style.display = "none"; // Ocultar por defecto

    const docSeleccionado = tipoDocumento.value;

    if (docSeleccionado === "PAGARE") {
        contenedorPagare.style.display = "block";
        actualizarVisibilidadPagare();
    } else if (docSeleccionado !== "") {
        // Si se selecciona un documento diferente a Pagaré y no está vacío
        contenedorNotariosDoc.style.display = "block";
    }
}

function actualizarVisibilidadPagare() {
    // Resetear visibilidad interna del pagaré
    contenedorFiadores.style.display = "none";
    contenedorCreditos.style.display = "none";

    const valorPagare = tipoPagare.value.toUpperCase();

    if (valorPagare === "FIADOR") {
        contenedorFiadores.style.display = "block";
    }
    if (valorPagare === "RESTRUCTURACION" || valorPagare === "REESTRUCTURACION") {
        contenedorCreditos.style.display = "block";
    }
}

// Asignar los eventos para cuando el usuario cambie las opciones manualmente
tipoDocumento.addEventListener("change", actualizarVisibilidadDocumento);
tipoPagare.addEventListener("change", actualizarVisibilidadPagare);

// ¡CRUCIAL! Ejecutar las funciones al cargar el script para el modo UPDATE
actualizarVisibilidadDocumento();

// --- AGREGAR FIADORES ---
$("#btnAgregarFiador").click(function() {
    const nuevaFila = $(`
        <div class="row mb-2 fila-fiador align-items-end">
            <div class="col-md-10">
                <select class="form-control fiador_select customer_id" style="width: 100%;"></select>
            </div>
            <div class="col-md-2">
                <button type="button" class="btn btn-danger btn-eliminar w-100">X</button>
            </div>
        </div>
    `);

    $("#lista_fiadores").append(nuevaFila);

    nuevaFila.find('.customer_id').select2({
        width: '100%',
        ajax: {
            url: urls_p.api_url_cliente,
            dataType: 'json',
            delay: 250,
            data: function (params) { return { term: params.term }; },
            processResults: function (data) {
                if (Array.isArray(data)) {
                    return {
                        results: data.map(function (item) {
                            return {
                                id: item.id,
                                text: `${item.customer_code} - ${item.first_name} ${item.last_name}`
                            };
                        })
                    };
                }
                return { results: [] };
            },
            cache: true
        },
        placeholder: 'Seleccione al Fiador',
        minimumInputLength: 1
    });
});

// --- AGREGAR CRÉDITOS VIGENTES ---
$("#btnAgregarCredito").click(function() {
    const nuevaFila = $(`
        <div class="row mb-2 fila-credito align-items-end">
            <div class="col-md-10">
                <select class="form-control credito_vigente" style="width: 100%;"></select>
            </div>
            <div class="col-md-2">
                <button type="button" class="btn btn-danger btn-eliminar w-100">X</button>
            </div>
        </div>
    `);

    $("#lista_creditos").append(nuevaFila);

    nuevaFila.find('.credito_vigente').select2({
        width: '100%',
        ajax: {
            url: urls_p.api_url_credit_vigente,
            dataType: 'json',
            delay: 250,
            data: function (params) { return { term: params.term }; },
            processResults: function (data) {
                if (Array.isArray(data)) {
                    return {
                        results: data.map(function (item) {
                            return {
                                id: item.id,
                                text: `ID: ${item.id} | Crédito: ${item.codigo_credito} (${item.customer_id.first_name} ${item.customer_id.last_name})`
                            };
                        })
                    };
                }
                return { results: [] };
            },
            cache: true
        },
        placeholder: 'Seleccione un Crédito Vigente',
        minimumInputLength: 1
    });
});

// --- AGREGAR GARANTÍAS ---
$("#btnAgregarGarantia").click(function() {
    const idUnico = 'notario_garantia_' + Date.now() + Math.floor(Math.random() * 100);
    
    $("#lista_garantias").append(`
        <div class="row mb-2 fila-garantia align-items-end p-2 border rounded bg-light">
            <div class="col-md-3">
                <label class="small text-muted">Tipo</label>
                <select class="form-control garantia-tipo">
                    <option value="HIPOTECA">HIPOTECA</option>
                    <option value="DERECHO DE POSESION HIPOTECA">DERECHO DE POSESION HIPOTECA</option>
                    <option value="CHEQUE / PAGARE">CHEQUE / PAGARE</option>
                    <option value="VEHICULO">VEHICULO</option>
                    <option value="MOBILIARIA">MOBILIARIA</option>
                </select>
            </div>
            <div class="col-md-3">
                <label class="small text-muted">Descripción</label>
                <input type="text" class="form-control garantia-descripcion" placeholder="Detalles de la garantía...">
            </div>
            <div class="col-md-2">
                <label class="small text-muted">Valor</label>
                <input type="number" step="0.01" class="form-control garantia-valor" placeholder="0.00">
            </div>
            
            <div class="col-md-3 contenedor-notario-garantia" style="display: none;">
                <label class="small text-danger fw-bold">Notario Asignado</label>
                <select class="form-control garantia-notario-select" id="${idUnico}" style="width: 100%;"></select>
            </div>
            
            <div class="col-md-1">
                <button type="button" class="btn btn-danger btn-eliminar w-100">X</button>
            </div>
        </div>
    `);

    // Inicializar Select2 en el nuevo selector creado para la fila
    $(`#${idUnico}`).select2({
        width: '100%',
        ajax: {
            url: urls_p.api_url_notario,
            dataType: 'json',
            delay: 250,
            data: function (params) { return { term: params.term }; },
            processResults: function (data) {
                return {
                    results: data.map(item => ({ id: item.id, text: item.nombre_completo || item.nombre }))
                };
            }
        },
        placeholder: 'Seleccione Notario'
    });
});

// Detectar cambios en Tipo y Valor de Garantías para evaluar la regla (> 5000 y CHEQUE / PAGARE)
$(document).on('change keyup', '.garantia-tipo, .garantia-valor', function() {
    const fila = $(this).closest('.fila-garantia');
    const tipo = fila.find('.garantia-tipo').val();
    const valor = parseFloat(fila.find('.garantia-valor').val()) || 0;
    const contenedorNotario = fila.find('.contenedor-notario-garantia');

    if (tipo === "CHEQUE / PAGARE" && valor > 500) {
        contenedorNotario.fadeIn();
    } else {
        contenedorNotario.fadeOut();
        fila.find('.garantia-notario-select').val(null).trigger('change'); // Limpiar selección si se oculta
    }
});

$(document).on('click', '.btn-eliminar', function() {
    $(this).closest('.row').remove();
});

function validarFormulario() {

    // ===============================
    // CAMPOS OBLIGATORIOS
    // ===============================

    if (!$("#asesor_responsable").val()) {
        Swal.fire({
            icon: "warning",
            title: "Campo requerido",
            text: "Debe seleccionar un asesor responsable."
        });
        return false;
    }

    if (!$("#type_of_product_or_service").val()) {
        Swal.fire({
            icon: "warning",
            title: "Campo requerido",
            text: "Debe seleccionar el tipo de producto."
        });
        return false;
    }

    if (!$("#forma_de_pago").val()) {
        Swal.fire({
            icon: "warning",
            title: "Campo requerido",
            text: "Debe seleccionar la forma de pago."
        });
        return false;
    }

    if (!$("#total_value_of_the_product_or_service").val()) {
        Swal.fire({
            icon: "warning",
            title: "Campo requerido",
            text: "Debe ingresar el valor del producto."
        });
        return false;
    }

    if (!$("#tasa_interes").val()) {
        Swal.fire({
            icon: "warning",
            title: "Campo requerido",
            text: "Debe ingresar la tasa de interés."
        });
        return false;
    }

    if (!$("#fecha_inicio").val()) {
        Swal.fire({
            icon: "warning",
            title: "Campo requerido",
            text: "Debe seleccionar la fecha de inicio."
        });
        return false;
    }

    if (!$("#plazo").val()) {
        Swal.fire({
            icon: "warning",
            title: "Campo requerido",
            text: "Debe ingresar el plazo."
        });
        return false;
    }

    if (!$("#tipo_documento").val()) {
        Swal.fire({
            icon: "warning",
            title: "Campo requerido",
            text: "Debe seleccionar el tipo de documento."
        });
        return false;
    }

    // ===============================
    // VALIDACIONES DE NEGOCIO
    // ===============================

    const formaPago = $("#forma_de_pago").val();
    const plazoGarantia = $("#plazo_garantia").val();

    if (
        (formaPago === "INTERES MENSUAL Y CAPITAL AL VENCIMIENTO" ||
         formaPago === "INTERES Y CAPITAL AL VENCIMIENTO") &&
        !plazoGarantia
    ) {
        Swal.fire({
            icon: "warning",
            title: "Campo requerido",
            text: "Debe ingresar el plazo de garantía."
        });
        return false;
    }

    if ($("#tipo_documento").val() === "PAGARE") {

        const tipoPagare = $("#tipo_pagare").val();

        if (!tipoPagare) {
            Swal.fire({
                icon: "warning",
                title: "Campo requerido",
                text: "Debe seleccionar el tipo de pagaré."
            });
            return false;
        }

        if (
            (tipoPagare === "FIADOR" || tipoPagare === "Fiador") &&
            $(".fiador_select").length === 0
        ) {
            Swal.fire({
                icon: "warning",
                title: "Campo requerido",
                text: "Debe agregar al menos un fiador."
            });
            return false;
        }

        let fiadorVacio = false;

        $(".fiador_select").each(function () {
            if (!$(this).val()) {
                fiadorVacio = true;
            }
        });

        if (fiadorVacio) {
            Swal.fire({
                icon: "warning",
                title: "Campo requerido",
                text: "Todos los fiadores deben estar seleccionados."
            });
            return false;
        }

        if (
            (tipoPagare === "REESTRUCTURACION" ||
             tipoPagare === "Restructuracion") &&
            $(".credito_vigente").length === 0
        ) {
            Swal.fire({
                icon: "warning",
                title: "Campo requerido",
                text: "Debe agregar al menos un crédito vigente."
            });
            return false;
        }

        let creditoVacio = false;

        $(".credito_vigente").each(function () {
            if (!$(this).val()) {
                creditoVacio = true;
            }
        });

        if (creditoVacio) {
            Swal.fire({
                icon: "warning",
                title: "Campo requerido",
                text: "Todos los créditos deben estar seleccionados."
            });
            return false;
        }
    }

    // Garantías

    if ($(".fila-garantia").length === 0) {
        Swal.fire({
            icon: "warning",
            title: "Campo requerido",
            text: "Debe registrar al menos una garantía."
        });
        return false;
    }

    let garantiaIncompleta = false;

    $(".fila-garantia").each(function () {

        if (
            !$(this).find(".garantia-tipo").val() ||
            !$(this).find(".garantia-descripcion").val().trim() ||
            !$(this).find(".garantia-valor").val()
        ) {
            garantiaIncompleta = true;
        }
    });

    if (garantiaIncompleta) {
        Swal.fire({
            icon: "warning",
            title: "Campo requerido",
            text: "Complete toda la información de las garantías."
        });
        return false;
    }

    
    const valorTotalProducto = parseFloat($("#total_value_of_the_product_or_service").val()) || 0;
    let sumaGarantias = 0;

    // Sumar el valor de cada fila de garantía registrada
    $(".fila-garantia").each(function () {
        const valorGarantia = parseFloat($(this).find(".garantia-valor").val()) || 0;
        sumaGarantias += valorGarantia;
    });

    // Validar que la suma de las garantías sea mayor o igual al valor del producto
    if (sumaGarantias < valorTotalProducto) {
        Swal.fire({
            icon: "error",
            title: "Garantías insuficientes",
            text: `El valor de las garantías (Q ${sumaGarantias.toFixed(2)}) debe ser mayor o igual al valor total del producto (Q ${valorTotalProducto.toFixed(2)}).`
        });
        return false;
    }

    if (valorTotalProducto >= 25000) {
        if (!$("#riesgo_comercial").val()) {
            Swal.fire({
                icon: "warning",
                title: "Campo requerido",
                text: "Debe poner los riesgos comerciales principales."
            });
            return false;
        }

        if (!$("#diganostico_oportunidad").val()) {
            Swal.fire({
                icon: "warning",
                title: "Campo requerido",
                text: "Debe poner el diagnóstico de oportunidades."
            });
            return false;
        }

        if (!$("#mitigadores").val()) {
            Swal.fire({
                icon: "warning",
                title: "Campo requerido",
                text: "Debe poner los mitigadores."
            });
            return false;
        }

        if (!$("#evaluacion_mercado").val()) {
            Swal.fire({
                icon: "warning",
                title: "Campo requerido",
                text: "Debe poner la evaluación del mercado."
            });
            return false;
        }
    }

    return true;
}

// 2. CORRECCIÓN: Agregado 'async' al callback del submit para poder usar 'await'
$("#frmInvestmentPlan").on("submit", async function(e) {
    e.preventDefault();

    if (!validarFormulario()) {
        return;
    }

    const estadoAprobacion = $("#estado_aprobacion").val();
    
    if (estadoAprobacion === "ACEPTADO") {
        // Ejecutamos la función de validación y esperamos su respuesta
        const codigoValido = await verificarCodigoSeguridad();
        if (!codigoValido) {
            return; // Detiene la ejecución si el código no es correcto o cancelan
        }
    }

    const planId = $("#investment_plan_id").val();

    
    let garantias = [];
    const listaNotariosPayload = []; // Tu lista global unificada

    // 1. Capturar Notario de Documentación (si aplica)
    if (tipoDocumento.value !== "PAGARE" && tipoDocumento.value !== "" && $("#notario_documentacion").val()) {
        listaNotariosPayload.push({
            'id': parseInt($("#notario_documentacion").val()),
            'nombre': $("#notario_documentacion").find('option:selected').text(),
            'modulo': 'documentacion'
        });
    }

    // 2. Recorrer Garantías
    $(".fila-garantia").each(function () {
        const tipo = $(this).find(".garantia-tipo").val();
        const descripcion = $(this).find(".garantia-descripcion").val();
        const valor = parseFloat($(this).find(".garantia-valor").val()) || 0;
        
        const selectNotario = $(this).find(".garantia-notario-select");
        let notarioGarantia = null;

        // Si cumple la condición, extraemos el notario de esta fila
        if (tipo === "CHEQUE / PAGARE" && valor > 5000 && selectNotario.val()) {
            notarioGarantia = {
                'id': parseInt(selectNotario.val()),
                'nombre': selectNotario.find('option:selected').text()
            };

            // También lo agregamos a la lista global histórica si tu backend lo requiere de ambos lados
            listaNotariosPayload.push({
                'id': notarioGarantia.id,
                'nombre': notarioGarantia.nombre,
                'modulo': 'garantia'
            });
        }

        garantias.push({
            tipo: tipo,
            descripcion: descripcion,
            valor: valor,
            notario: notarioGarantia // <--- El notario ahora vive de forma nativa en la garantía
        });
    });
   

    const fiadores = [];
    $(".fiador_select").each(function() {
        if ($(this).val()) {
            fiadores.push({
                "id": parseInt($(this).val())
            });
        }
    });

    // CAMBIO AQUÍ: Ahora guarda una lista de objetos con la estructura {"id": X}
    const creditos = [];
    $(".credito_vigente").each(function() {
        if ($(this).val()) {
            creditos.push({
                "id": parseInt($(this).val())
            });
        }
    });

    // Nota sobre total_value_of_the_product_or_service: Como lo removiste del HTML 
    // y tu modelo lo exige (null=False), usaré provisionalmente el initial_amount o 0 para que no falle.
    const montoInicial = $("#total_value_of_the_product_or_service").val() ? parseFloat($("#total_value_of_the_product_or_service").val()) : 0.00;

    const payload = {
        customer_id: parseInt($("#customer_id").val()), // Llave foránea (ID entero)
        sucursal: parseInt($("#sucursal").val()),
        type_of_product_or_service: $("#type_of_product_or_service").val(),
        total_value_of_the_product_or_service: montoInicial, // Ajustar según lógica de negocio si cambia
        initial_amount: montoInicial,
        monthly_amount:montoInicial,
        
        fecha_inicio: $("#fecha_inicio").val() || null,
        plazo: $("#plazo").val() ? parseInt($("#plazo").val()) : null,
        plazo_gracia: $("#plazo_garantia").val() ? parseInt($("#plazo_garantia").val()) : null,
        forma_de_pago: $("#forma_de_pago").val(),
        transfers_or_transfer_of_funds: true,
        type_of_transfers_or_transfer_of_funds: "Local", // Satisface los choices del modelo si se requiere

        tasa_interes: $("#tasa_interes").val() ? parseFloat($("#tasa_interes").val()) : null,
        tipo_documento: $("#tipo_documento").val() || null,
        tipo_pagare: $("#tipo_pagare").val() || null,
        
        // 3. CORRECCIÓN: Se agregó el '#' faltante para recuperar el textarea
        investment_plan_description: $("#investment_plan_description").val() || "",
        riesgo_comercial: $("#riesgo_comercial").val() || "",
        diganostico_oportunidad: $("#diganostico_oportunidad").val() || "",
        mitigadores: $("#mitigadores").val() || "",
        evaluacion_mercado: $("#evaluacion_mercado").val() || "",
        
        // Atributos estructurados mapeados a tus JSONFields
        fiador: fiadores,
        credito_anterior_vigente: creditos,
        garantias: garantias,
        asesor_responsable:  parseInt($("#asesor_responsable").val()),
        estado_aprobacion: $("#estado_aprobacion").val(),
        notarios: listaNotariosPayload
    };

    console.log("Payload enviado en JSON:", payload);

    try {
        // 4. CORRECCIÓN: Invocación correcta pasando el payload estructurado
        const resultado = await savePlanInversion(payload, planId ? planId : null);
         Swal.fire({
            icon: "success",
            title: "Registro Completado",
         
            timer: 500,
            showConfirmButton: false,
        });
        let codigo_cliente = document.getElementById('codigo_cliente').value;
        setTimeout(() => { window.location.href = `/customers/detail/${codigo_cliente}/`; }, 1000);
        // Aquí puedes redirigir, p. ej.: window.location.href = '/planes/';
    } catch (err) {
        Swal.fire({
            icon: "error",
            title: "Error",
            text: err,
            timer: 7000,
            showConfirmButton: false,
        });
        console.error(e);
    }
});


