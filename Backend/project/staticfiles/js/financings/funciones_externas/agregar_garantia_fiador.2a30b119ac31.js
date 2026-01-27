import { Fiador } from '../../class/type_guarantee.js';

import { ocultar } from './ocultar_mostrar.js'
import { clearFields } from './limpiador.js'

import {get_cliente} from '../../API/customer/get_customer.js'



// Evento para agregar una hipoteca
export function agregar_fiador(addGuarantee) {
    document.getElementById('agregar_garantiaF').addEventListener('click', async function (event) {
        event.preventDefault();

        let valor_cobertura = document.getElementById('valor_cobertura').value;
        if (!valor_cobertura || valor_cobertura === '') {
            alert('DEBE DE INGRESAR EL VALOR DE COBERTURA');
            return;
        }

        const fiador = new Fiador();
        let customer_id = document.getElementById('customer_id_fiador').value;

        try {
            const cliente = await get_cliente(customer_id);

            fiador.nombre = `${cliente.first_name} ${cliente.last_name}`;
            fiador.codigo_cliente = document.getElementById('fiador_codigo_cliente').value;
            fiador.numeroTelefono = document.getElementById('telefono2').value;
            fiador.lugar_trabajo = document.getElementById('lugar_trabajo').value;
            fiador.ingresos = document.getElementById('ingreso').value;
            // fiador.fotografia = document.getElementById('fotografiaF').files[0];

            addGuarantee('FIADOR', fiador.toJSON());
            clearFields();
            ocultar(document.getElementById('fiador'));
            document.getElementById('tipo_garantia').value = 0;

        } catch (error) {
            console.error('Error al obtener cliente:', error);
            alert('No se pudo obtener la información del cliente fiador.');
        }
    });
}

