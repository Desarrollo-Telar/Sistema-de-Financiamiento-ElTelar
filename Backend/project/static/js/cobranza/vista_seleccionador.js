import { urls_p } from '../API/urls_api.js'
import { get_credit } from '../API/credito/obtener_credito.js'
import { get_ultima_cuota_ampliacion } from '../API/credito/obtener_ultima_cuota.js'

const selectedCreditId = $(".credito_vigente").val();



$(document).ready(async  function () {
    const selectedCreditId = $(".credito_vigente").val();

    if (!selectedCreditId) {
        console.warn("No se ha seleccionado ningún crédito.");
        return;
    }

    try {
        // Obtener la última cuota activa o de ampliación del crédito
        const cuotas = await get_ultima_cuota_ampliacion(selectedCreditId);
        const cuota = cuotas?.[0];

        if (!cuota) {
            console.warn("No se encontró una cuota válida para el crédito.");
            return;
        }

        console.log("Cuota obtenida:", cuota);

        // Calcular el total pendiente (saldo + interés + mora)
        const saldo = parseFloat((cuota.saldo_pendiente || "0").toString().replace(/,/g, '')) || 0;
        const interes = parseFloat((cuota.interest || "0").toString().replace(/,/g, '')) || 0;
        const mora = parseFloat((cuota.mora || "0").toString().replace(/,/g, '')) || 0;

        const total_pendiente = saldo + interes + mora;

        // Asignar valores al formulario
        $('#id_monto_pendiente').val(total_pendiente.toFixed(2));
        $('#id_mora_pendiente').val(mora.toFixed(2));
        $('#id_interes_pendiente').val(interes.toFixed(2));
        $('#id_fecha_limite_cuota').val(cuota.fecha_limite_d);

        // Obtener teléfono del cliente si está disponible
        const telefono = cuota.credit_id?.customer_id?.telephone || '';
        $('#id_telefono_contacto').val(telefono);

    } catch (error) {
        console.error('Error obteniendo detalles del crédito:', error);
    }
    $(".credito_vigente").select2({
        width: 'resolve',
        ajax: {
            url: urls_p.api_url_credit_vigente_cobranza,
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    term: params.term // Parámetro que el backend debe esperar
                };
            },
            data: function (params) {
                return {
                    term: params.term // Parámetro que el backend debe esperar
                };
            },
            processResults: function (data) {
                console.log(data);
                // Verificar si 'data' es un array de objetos
                if (Array.isArray(data)) {
                    return {
                        results: data.map(function (item) {
                            console.log(item);
                            return {
                                id: item.id,
                                text: item.codigo_credito + ' ' + item.customer_id.first_name + ' ' + item.customer_id.last_name
                            };
                        })
                    };
                } else {
                    console.error('Estructura de datos inesperada:', data);
                    return {
                        results: []
                    };
                }
            },
            cache: true
        },
        placeholder: 'Seleccione un Credito Vigente',
        minimumInputLength: 1
    });
    $(".credito_vigente").on('select2:select', async function (e) {
        let data = e.params.data;

        try {
            // Obtener información del crédito seleccionado
            const credito_v = await get_credit(data.id);

            if (!credito_v || !credito_v.customer_id) {
                console.warn("Información de crédito incompleta:", credito_v);
                return;
            }

            console.log(`Crédito de: ${credito_v.customer_id.first_name} ${credito_v.customer_id.last_name}`);

            // Obtener la última cuota activa o de ampliación del crédito
            const cuotas = await get_ultima_cuota_ampliacion(credito_v.id);
            const cuota = cuotas?.[0];

            if (!cuota) {
                console.warn("No se encontró una cuota válida para el crédito.");
                return;
            }

            console.log("Cuota obtenida:", cuota);

            // Calcular el total pendiente (saldo + interés + mora)
            const saldo = parseFloat((cuota.saldo_pendiente || "0").replace(/,/g, '')) || 0;
            const interes = parseFloat((cuota.interest || "0").replace(/,/g, '')) || 0;
            const mora = parseFloat((cuota.mora || "0").replace(/,/g, '')) || 0;

            const total_pendiente = saldo + interes + mora;

            console.log(saldo);

            // Asignar valores a los campos del formulario
            //document.getElementById('id_cuota').value = cuota;
            document.getElementById('id_monto_pendiente').value = total_pendiente.toFixed(2);
            document.getElementById('id_mora_pendiente').value = mora.toFixed(2);
            document.getElementById('id_interes_pendiente').value = interes.toFixed(2);
            //document.getElementById('id_fecha_limite_cuota').disabled = false;
            document.getElementById('id_fecha_limite_cuota').value = cuota.fecha_limite_d;
            console.log( cuota.fecha_limite_d)

            // Obtener teléfono del cliente
            const telefono = cuota.credit_id?.customer_id?.telephone || '';
            document.getElementById('id_telefono_contacto').value = telefono;

        } catch (error) {
            console.error('Error obteniendo detalles del crédito:', error);
        }
    });


});