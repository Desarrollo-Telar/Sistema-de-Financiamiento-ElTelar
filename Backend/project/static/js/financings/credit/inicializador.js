import {actualizarTotalDepositar} from './desembolso.js'
import {urls_p} from '../../API/urls_api.js'
import {seleccion_garantia, seleccion_desembolso} from '../funciones_externas/seleccionador.js'
import {ocultar, mostrar} from '../funciones_externas/ocultar_mostrar.js'
// FILTROS 
import { get_ultima_cuota_ampliacion } from '../../API/credito/obtener_ultima_cuota.js'
import {get_credit} from '../../API/credito/obtener_credito.js'
import { actualizar_credito } from '../../API/credito/actualizar.js'


const plazo = document.getElementById('plazo');
const fecha_inicio = document.getElementById('fecha_inicio');
const fecha_vencimiento = document.getElementById('fecha_vencimiento');
const monto_credito_vigente = document.getElementById('monto_credito_vigente');
const saldo_capital_credito_vigente = document.getElementById('saldo_capital_credito_vigente');
const honorarios_desembolso = document.getElementById('honorarios_desembolso');
const poliza_seguro_desembolso = document.getElementById('poliza_seguro_desembolso');
const monto_desembolsado_desembolsar = document.getElementById('monto_desembolsado_desembolsar');
const total_a_desembolsar = document.getElementById('total_a_desembolsar');
seleccion_garantia();
seleccion_desembolso();

// Obtener el protocolo (HTTP/HTTPS)
const protocolo = window.location.protocol; // Ejemplo: "https:"

// Obtener el dominio (hostname)
const dominio = window.location.hostname; // Ejemplo: "example.com"

// Obtener el puerto
const puerto = window.location.port; // Ejemplo: "8080" o "" si no está explícito
const baseUrl = `${protocolo}//${dominio}${puerto ? `:${puerto}` : ''}`;

fecha_inicio.addEventListener('input', function (event) {
    const plazoValue = parseInt(plazo.value, 10); // Obtén el valor del plazo
    const fechaInicioValue = new Date(event.target.value);
    if (!isNaN(plazoValue) && fechaInicioValue instanceof Date && !isNaN(fechaInicioValue)) {
        fechaInicioValue.setMonth(fechaInicioValue.getMonth() + plazoValue);
        fecha_vencimiento.value = fechaInicioValue.toISOString().split('T')[0];
    }
});

plazo.addEventListener('input', function (event) {
    const plazoValue = parseInt(event.target.value, 10); // Obtén el valor del plazo
    const fechaInicioValue = new Date(fecha_inicio.value);
    if (!isNaN(plazoValue) && fechaInicioValue instanceof Date && !isNaN(fechaInicioValue)) {
        fechaInicioValue.setMonth(fechaInicioValue.getMonth() + plazoValue);
        fecha_vencimiento.value = fechaInicioValue.toISOString().split('T')[0];
        console.log(fechaInicioValue.toISOString().split('T')[0]);
    }
});



$(document).ready(function () {
    $('.asesor').select2({
        ajax: {
            url:  `${baseUrl}/customers/api/asesores/`,
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
    $(".credito_vigente").on('select2:select', async function (e) {
        let data = e.params.data;
        try{
            // Obtener toda la informacion relacionada con el credito vigente seleccionado
            const credito_v = await get_credit(data.id);
            
            if (credito_v.id ==1){
                const formData = new FormData();
                formData.append('is_paid_off', false);

                actualizar_credito(credito_v.id, formData);

            }
            
            // Obtener la ultima cuota vigente para el credito vigente seleccionado
            const cuotas = await get_ultima_cuota_ampliacion(credito_v.id);
            const cuota = cuotas[0];

            // Mostrando la informacion relevante al credito vigente seleccionado
            const informacion_credito = document.getElementById('informacion_credito');
            informacion_credito.style.display = 'block';
            informacion_credito.innerHTML = `
            <p>Saldo Capital Pendiente: ${cuota.saldo_pendiente} </p>
            <p>Intereses: ${cuota.interest} </p>
            <p>Mora: ${cuota.mora} </p>
            <p>Plazo del Credito: ${credito_v.plazo} Meses </p>
            <hr>
            <p>Saldo Actual: ${credito_v.Fsaldo_actual} </p>
            `
            

            // Habilitar que se muestre los divs
            mostrar(monto_credito_vigente);
            mostrar(saldo_capital_credito_vigente);
            mostrar(honorarios_desembolso);
            mostrar(poliza_seguro_desembolso);
            mostrar(monto_desembolsado_desembolsar);
            mostrar(total_a_desembolsar);

            // Asignando valores a credito vigente
            document.getElementById('credito_monto_vigente').value = credito_v.monto;
            document.getElementById('credito_saldo_capital_vigente').value = credito_v.saldo_actual;
            actualizarTotalDepositar();

        }catch(error){
            console.error('Error obteniendo detalles del credito:', error);
        }
        
    });
    $(".customer_id_fiador").select2({
        width: 'resolve',
        ajax: {
            url:  urls_p.api_url_cliente,

            dataType: 'json',
            delay: 250,
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
    async function fetchInformacion_laboral() {

        return fetch(urls_p.api_url_informacion_laboral)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al momento de obtener informacion laboral ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log('Lista de clientes de informacion laboral obtenida:', data);
                return data; // Puedes devolver los datos si necesitas hacer algo con ellos
            })
            .catch(error => {
                console.error('Error al obtener la lista de clientes:', error);
                throw error; // Puedes relanzar el error para manejarlo en otra parte de tu aplicación si es necesario
            });

    }
    async function fetchOtraInformacion_laboral() {

        return fetch(urls_p.api_url_otra_informacion_laboral)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al momento de obtener informacion laboral ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log('Lista de clientes obtenida:', data);
                return data; // Puedes devolver los datos si necesitas hacer algo con ellos
            })
            .catch(error => {
                console.error('Error al obtener la lista de clientes:', error);
                throw error; // Puedes relanzar el error para manejarlo en otra parte de tu aplicación si es necesario
            });

    }

    async function filtro(valor) {
        try {
            const laboral = await fetchInformacion_laboral();
            const otra = await fetchOtraInformacion_laboral();

            let filterList = [];

            if (laboral && laboral.length > 0) {
                filterList = laboral.filter(item => item['customer_id'] === valor);
            }

            if (filterList.length === 0 && otra && otra.length > 0) {
                filterList = otra.filter(item => item['customer_id'] === valor);
            }

            console.log(filterList);
            return filterList;

        } catch (error) {
            console.error('Error en el filtro', error);
            throw error;
        }
    }


    $(".customer_id_fiador").on('select2:select', async function (e) {
        var data = e.params.data;
        var clienteId = data.id;
        var codigo_cliente = document.getElementById('fiador_codigo_cliente');
        var telefono = document.getElementById('telefono2');
        var lugar_trabajo = document.getElementById('lugar_trabajo');
        var ingreso = document.getElementById('ingreso');

        try {
            const laboral = await filtro(clienteId);
            laboral.forEach(element => {
                if (element.company_name) {
                    lugar_trabajo.value = element.company_name;

                } else {
                    lugar_trabajo.value = element.source_of_income;
                }

                ingreso.value = element.salary;
                console.log(element);
            });

            // Realizar una solicitud para obtener detalles adicionales del cliente
            const response = await fetch(`${urls_p.api_url_cliente}${clienteId}/`);
            if (!response.ok) {
                throw new Error(`Error en la solicitud: ${response.statusText}`);
            }
            const clienteDetalles = await response.json();
            codigo_cliente.value = clienteDetalles.customer_code;
            telefono.value = clienteDetalles.telephone;
            // Aquí puedes usar los detalles de cliente para llenar otros campos, como lugar_trabajo e ingreso
        } catch (error) {
            console.error('Error obteniendo detalles del cliente:', error);
        }
    });

});






