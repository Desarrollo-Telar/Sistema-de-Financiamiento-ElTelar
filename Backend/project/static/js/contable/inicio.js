import {urls_p} from '../API/urls_api.js'

$(document).ready(function () {
    $(".credito_vigente").select2({
        width: 'resolve',
        ajax: {
            url: urls_p.api_url_credit,
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

});