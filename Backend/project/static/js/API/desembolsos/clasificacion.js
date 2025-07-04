
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
const div_monto_credito_agregar = document.getElementById('div_monto_credito_agregar');
const div_monto_credito_cancelar = document.getElementById('div_monto_credito_cancelar');
const informacion_credito = document.getElementById('informacion_credito');

let codigo_credito = null;

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



const credito_monto = document.getElementById('monto_credito');


let credit_id, saldo_anterior = 0, suma = 0;
//const saldo = document.getElementById('saldo_anterior');
// Función para obtener valor numérico de un campo por ID
const obtenerValorNumerico = (id) => parseFloat(document.getElementById(id)?.value) || 0;
// Agrega event listeners a los campos relevantes
const campos = ['monto_credito', 'poliza_seguro', 'honorarios', 'monto_credito_agregar', 'saldo_anterior'];
campos.forEach(id => {
    const elemento = document.getElementById(id);
    if (elemento) {
        elemento.addEventListener('input', actualizarTotalDepositar);
    }
});

async function actualizarTotalDepositar() {
    
    const monto = obtenerValorNumerico('monto_credito');
    const poliza_seguro = obtenerValorNumerico('poliza_seguro');
    const honorarios = obtenerValorNumerico('honorarios');
    const monto_credito_agregar = obtenerValorNumerico('monto_credito_agregar');
    
    const saldo_anterior = obtenerValorNumerico('saldo_anterior');

    let monto_total = monto + monto_credito_agregar;
    suma = 0;
    let total_depositars = parseFloat(monto_total - (saldo_anterior+poliza_seguro+honorarios)).toFixed(2);
    document.getElementById('total_depositar').value = total_depositars;
       

    // Actualiza los valores en el objeto desembolso
    //Object.assign(desembolso, { monto_credito: total, poliza_seguro, honorarios, saldo_anterior });



    
}

document.getElementById('forma_desembolso')?.addEventListener('change', async (event) => {
    const valorSeleccionado = event.target.value;
    const credito = await get_credit(credit_id);

    if (!valorSeleccionado) throw new Error('Opción no seleccionada');
    credito_monto.value = credito.monto;


    switch (valorSeleccionado) {
        case 'APLICACIÓN DE AMPLIACIÓN DE CRÉDITO VIGENTE':
            mostrar();
            //desembolso.forma_desembolso = valorSeleccionado;
            

            //console.log(desembolso.forma_desembolso);
            div_monto_credito_cancelar.style.display = 'none';
            div_monto_credito_agregar.style.display = 'block';
            
            document.getElementById('monto_credito_agregar').addEventListener('input', actualizarTotalDepositar);
            await actualizarTotalDepositar();

            break;

        case 'CANCELACIÓN DE CRÉDITO VIGENTE':
            //desembolso.forma_desembolso = valorSeleccionado;
            //console.log(desembolso.forma_desembolso);
            mostrar();
            
            document.getElementById('monto_credito_agregar').value = 0; // Limpia el valor
            div_monto_credito_agregar.style.display = 'none';
            div_plazo_restante.style.display = 'none';
            div_monto_credito_cancelar.style.display = 'block';
            await actualizarTotalDepositar();


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
            document.getElementById('saldo_pendiente_credito').value = credito.saldo_pendiente;
            document.getElementById('plazo_credito').value = credito.plazo;
            document.getElementById('plazo_credito_restante').value = credito.plazo_restante;
            document.getElementById('tasa_interes_credito').value = credito.tasa_interes;
            const cuota = await get_ultima_cuota(credito.id);
            informacion_credito.innerHTML = `
            <p>Saldo Capital Pendiente: ${cuota.saldo_pendiente} </p>
            <p>Intereses: ${cuota.interest} </p>
            <p>Mora: ${cuota.mora} </p>
            <p>Plazo del Credito: ${credito.plazo} Meses </p>
            <p>Plazo Restante del Credito: ${credito.plazo_restante} Meses </p>
            <hr>
            <p>Saldo Anterior: ${credito.Fsaldo_actual} </p>
            `

            div_forma_desembolso.style.display = 'block';


            // Actualizar saldo anterior
            document.getElementById('saldo_anterior').value = credito.saldo_actual;
            const monto_credito = parseFloat(credito.monto);

            credito_monto.value = credito.monto;


            const laboral = await get_desembolsos(credito.codigo_credito);
            codigo_credito = credito.codigo_credito;
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
