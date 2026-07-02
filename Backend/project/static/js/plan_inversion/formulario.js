const tipoDocumento = document.getElementById("tipo_documento");
const tipoPagare = document.getElementById("tipo_pagare");
const contenedorPagare = document.getElementById("contenedor_pagare");
const contenedorFiadores = document.getElementById("contenedor_fiadores");
const contenedorCreditos = document.getElementById("contenedor_creditos");

import { urls_p } from '../API/urls_api.js'
const URL = urls_p.api_url_investment_plan;

// 1. CORRECCIÓN: Cambiado headers a application/json para soportar los JSONFields cómodamente
export async function postPlanInversion(formData) {
    try {
        const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');
        if (!csrfTokenElement) {
            throw new Error('CSRF token not found');
        }
        const csrfToken = csrfTokenElement.getAttribute('content');

        const response = await axios({
            method: 'post',
            url: URL,
            headers: {
                'Content-Type': 'application/json', // Cambiado para enviar el objeto estructurado nativamente
                'X-CSRFToken': csrfToken
            },
            data: formData // Aquí viaja el payload directo
        });

        console.log("Plan guardado con éxito:", response.data);
        return response.data;
    } catch (error) {
        console.error(error);
        if (error.response) {
            console.error('Error en la respuesta del servidor:', error.response.data);
            console.error('Código de estado:', error.response.status);
        } else if (error.request) {
            console.error('Error en la solicitud (no hubo respuesta):', error.request);
        } else {
            console.error('Error:', error.message);
        }
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
            <div class="col-md-5">
                <label class="small text-muted">Descripción</label>
                <input type="text" class="form-control garantia-descripcion" placeholder="Detalles de la garantía...">
            </div>
            <div class="col-md-3">
                <label class="small text-muted">Valor</label>
                <input type="number" step="0.01" class="form-control garantia-valor" placeholder="0.00">
            </div>
            <div class="col-md-1">
                <button type="button" class="btn btn-danger btn-eliminar w-100">X</button>
            </div>
        </div>
    `);
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

    return true;
}

// 2. CORRECCIÓN: Agregado 'async' al callback del submit para poder usar 'await'
$("#frmInvestmentPlan").on("submit", async function(e) {
    e.preventDefault();

    if (!validarFormulario()) {
        return;
    }

    const garantias = [];
    $(".fila-garantia").each(function() {
        garantias.push({
            tipo: $(this).find(".garantia-tipo").val(),
            descripcion: $(this).find(".garantia-descripcion").val(),
            valor: parseFloat($(this).find(".garantia-valor").val()) || 0.00
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
        
        // Atributos estructurados mapeados a tus JSONFields
        fiador: fiadores,
        credito_anterior_vigente: creditos,
        garantias: garantias,
        asesor_responsable:  parseInt($("#asesor_responsable").val()),
        estado_aprobacion: $("#estado_aprobacion").val()
    };

    console.log("Payload enviado en JSON:", payload);

    try {
        // 4. CORRECCIÓN: Invocación correcta pasando el payload estructurado
        const resultado = await postPlanInversion(payload);
         Swal.fire({
            icon: "success",
            title: "Registro Completado",
         
            timer: 5000,
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