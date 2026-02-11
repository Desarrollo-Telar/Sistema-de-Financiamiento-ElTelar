import {urls_p} from '../../API/urls_api.js'


$(document).ready(function () {
   
    $(".customer_id").select2({
        width: 'resolve',
        ajax: {
            url: urls_p.api_url_clientes_aceptados,
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
    $('.asesor').select2({
        ajax: {
            url:  urls_p.api_url_asesores_credito,
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
                            console.log(item);
                            return {
                                id: item.id,
                                text: item.nombre + ' '+item.apellido
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
        placeholder: 'Seleccione un Asesor',
        minimumInputLength: 1

    });
    

   


    

});

