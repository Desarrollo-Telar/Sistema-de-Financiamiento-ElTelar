
import { generar_plan } from './funciones/tabla_pagos.js'
import { ocultar, mostrar } from '../financings/funciones_externas/ocultar_mostrar.js'
import { urls_p } from '../API/urls_api.js'
document.getElementById('generar_plan').onclick = generar_plan;

//id_tipo_pagare

const tipo_pagare = document.getElementById('id_tipo_pagare');


$(document).ready(function () {
    $(".customer_id").select2({
        width: 'resolve',
        ajax: {
            url: urls_p.api_url_cliente,
            dataType: 'json',
            delay: 250,
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
                            return {
                                id: item.id,
                                text: item.customer_code + ' ' + item.first_name + ' ' + item.last_name
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
        placeholder: 'Seleccione un Cliente',
        minimumInputLength: 1
    });
    $(".credito_vigente").select2({
        width: 'resolve',
        ajax: {
            url: urls_p.api_url_credit_vigente,
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
})