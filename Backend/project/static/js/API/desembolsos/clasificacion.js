
import { get_credit } from '../credito/obtener_credito.js';
import { get_ultima_cuota } from '../credito/obtener_ultima_cuota.js';
import { get_desembolsos } from '../desembolsos/filtro.js';
import { urls_p } from '../urls_api.js'
import { alerta_m } from '../../alertas/alertas.js'



const div_forma_desembolso = document.getElementById('div_forma_desembolso');
const add_Desembolso = document.getElementById('add_Desembolso');
const div_monto_credito = document.getElementById('div_monto_credito');
const div_saldo_anterior = document.getElementById('div_saldo_anterior');
const div_honorarios = document.getElementById('div_honorarios');
const div_poliza_seguro = document.getElementById('div_poliza_seguro');
const div_total_depositar = document.getElementById('div_total_depositar');
const div_plazo_restante = document.getElementById('div_plazo_restante');

const informacion_credito = document.getElementById('informacion_credito');


function mostrar() {
    add_Desembolso.style.display = 'block';
    div_monto_credito.style.display = 'block';
    div_saldo_anterior.style.display = 'block';
    div_honorarios.style.display = 'block';
    div_poliza_seguro.style.display = 'block';
    div_total_depositar.style.display = 'block';
    div_plazo_restante.style.display = 'block';
}
function ocultar() {
    add_Desembolso.style.display = 'none';
    div_monto_credito.style.display = 'none';
    div_saldo_anterior.style.display = 'none';
    div_honorarios.style.display = 'none';
    div_poliza_seguro.style.display = 'none';
    div_total_depositar.style.display = 'none';
    div_plazo_restante.style.display = 'none';

}

function generar(){
    // Crear el contenedor principal
const divMontoAgregado = document.createElement('div');
divMontoAgregado.classList.add('form-group');
divMontoAgregado.style.marginTop = '2rem';
divMontoAgregado.id = 'monto_agregado';

// Crear y configurar el label
const labelMontoSumar = document.createElement('label');
labelMontoSumar.classList.add('fw-medium');
labelMontoSumar.setAttribute('for', 'monto_sumar');
labelMontoSumar.textContent = 'Monto por agregar';

// Crear el contenedor del grupo de entrada
const divInputGroup = document.createElement('div');
divInputGroup.classList.add('input-group', 'mb-3');

// Crear el span del prefijo
const spanInputGroupText = document.createElement('span');
spanInputGroupText.classList.add('input-group-text', 'fw-medium');
spanInputGroupText.setAttribute('id', 'basic-addon1');
spanInputGroupText.textContent = 'Q';

// Crear el campo de entrada
const inputMontoSumar = document.createElement('input');
inputMontoSumar.type = 'number';
inputMontoSumar.min = '0';
inputMontoSumar.step = 'any';
inputMontoSumar.classList.add('form-control');
inputMontoSumar.id = 'monto_sumar';

// Construir la estructura
divInputGroup.appendChild(spanInputGroupText);
divInputGroup.appendChild(inputMontoSumar);

divMontoAgregado.appendChild(labelMontoSumar);
divMontoAgregado.appendChild(divInputGroup);

// Agregar el nuevo contenedor al div original
div_monto_credito.appendChild(divMontoAgregado);


}

const credito_monto = document.getElementById('monto');


let credit_id, saldo_anterior=0;
//const saldo = document.getElementById('saldo_anterior');
// Función para obtener valor numérico de un campo por ID
const obtenerValorNumerico = (id) => parseFloat(document.getElementById(id)?.value) || 0;
// Agrega event listeners a los campos relevantes
const campos = ['monto', 'poliza_seguro', 'honorarios', 'monto_sumar', 'saldo_anterior'];
campos.forEach(id => {
    const elemento = document.getElementById(id);
    if (elemento) {
        elemento.addEventListener('input', actualizarTotalDepositar);
    }
});

async function actualizarTotalDepositar() {
    const monto = obtenerValorNumerico('monto');
    const poliza_seguro = obtenerValorNumerico('poliza_seguro');
    const honorarios = obtenerValorNumerico('honorarios');
    const agg = obtenerValorNumerico('monto_sumar');
    const total = monto + agg;

    // Actualiza los valores en el objeto desembolso
    Object.assign(desembolso, { monto_credito: total, poliza_seguro, honorarios, saldo_anterior });

    suma = 0;

    try {
        const laboral = await filtro(credi_id);

        if (Array.isArray(laboral)) {
            suma = laboral.reduce((acum, el) => acum + parseFloat(el.monto_total_desembolso), 0);
        }

        if (suma >= total) {
            alert('NO SE PUEDE REALIZAR OTRO DESEMBOLSO');
            const addDesembolsoElement = document.getElementById('add_Desembolso');
            if (addDesembolsoElement) {
                addDesembolsoElement.style.display = 'none';
            }
            return;
        }

        document.getElementById('total_depositar').value = parseFloat(desembolso.total_a_depositar).toFixed(2);
        const addDesembolsoElement = document.getElementById('add_Desembolso');
        if (addDesembolsoElement) {
            addDesembolsoElement.style.display = '';
        }
    } catch (error) {
        console.error('Error obteniendo detalles del cliente:', error);
    }
}

document.getElementById('forma_desembolso')?.addEventListener('change', async (event) => {
    const valorSeleccionado = event.target.value;
    const credito = await get_credit(credit_id);


    const montoAgregado = document.getElementById('monto_agregado');

    if (!valorSeleccionado) throw new Error('Opción no seleccionada');
    credito_monto.value = credito.monto;


    switch (valorSeleccionado) {
        case 'APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE':
            mostrar();
            //desembolso.forma_desembolso = valorSeleccionado;


            //console.log(desembolso.forma_desembolso);

            // Añade el campo solo si no existe
            if (!montoAgregado) {
                generar();


                // Añade el listener después de crear el campo
                document.getElementById('monto_sumar').addEventListener('input', actualizarTotalDepositar);
            } else {
                montoAgregado.style.display = 'block';
            }

            break;

        case 'CANCELACIÓN DE CRÉDITO VIGENTE':
            //desembolso.forma_desembolso = valorSeleccionado;
            //console.log(desembolso.forma_desembolso);
            mostrar();

            // Oculta y limpia el campo `monto_sumar` si ya existe
            if (montoAgregado) {
                document.getElementById('monto_sumar').value = ''; // Limpia el valor
                montoAgregado.style.display = 'none';
            }

            break;
        default:
            ocultar();

    }
});


$(document).ready(function () {


    var suma = 0;

    $(".credit").on('select2:select', async function (e) {
        var data = e.params.data;
        credit_id = data.id;

        suma = 0; // Reiniciar suma para cada cálculo

        try {

            const credito = await get_credit(credit_id);
            const cuota = await get_ultima_cuota(credito.id);
            informacion_credito.innerHTML = `
            <p>Saldo Capital Pendiente: ${cuota.saldo_pendiente} </p>
            <p>Intereses: ${cuota.interest} </p>
            <p>Mora: ${cuota.mora} </p>
            <p>Plazo del Credito: ${credito.plazo} Meses </p>
            <hr>
            <p>Saldo Anterior: ${credito.Fsaldo_actual} </p>
            `

            div_forma_desembolso.style.display = 'block';


            // Actualizar saldo anterior
            document.getElementById('saldo_anterior').value = credito.saldo_actual;
            const monto_credito = parseFloat(credito.monto);
            document.getElementById('plazo_restante').value = credito.plazo_restante;
            credito_monto.value = credito.monto;


            const laboral = await get_desembolsos(credito.codigo_credito);
            console.log(laboral);



            if (Array.isArray(laboral)) {
                laboral.forEach(element => {
                    suma += parseFloat(element['monto_total_desembolso']);

                });
            }




            if (suma >= monto_credito) {
                alerta_m('NO SE PUEDE REALIZAR OTRO DESEMBOLSO', false);
                //window.location.href = '/financings/disbursement/';
            }

            console.log('Suma total de desembolsos:', suma);


            // Aquí puedes usar los detalles de cliente para llenar otros campos, como lugar_trabajo e ingreso
        } catch (error) {
            console.error('Error obteniendo detalles del credito:', error);
        }
    });

    $(".credit").select2({
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
            processResults: function (data) {
                console.log(data);
                if (Array.isArray(data)) {
                    return {
                        results: data.map(function (item) {

                            // Retornar resultado para Select2
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
        placeholder: 'Seleccione un Credito',
        minimumInputLength: 1
    });
});
