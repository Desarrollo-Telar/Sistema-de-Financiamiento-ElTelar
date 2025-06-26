import { Fiador } from '../../class/type_guarantee.js';

import { ocultar } from './ocultar_mostrar.js'
import { clearFields } from './limpiador.js'

// Evento para agregar una hipoteca
export function agregar_fiador(addGuarantee) {
    // Evento para agregar un Fiador
    document.getElementById('agregar_garantiaF').addEventListener('click', function (event) {
        event.preventDefault();

        let valor_cobertura = document.getElementById('valor_cobertura').value;
        if (!valor_cobertura || valor_cobertura === '') {
            alert('DEBE DE INGRESAR EL VALOR DE COBERTURA');
            return; // Cambiado para evitar el uso de `throw` en un evento DOM
        }
        const fiador = new Fiador()

        fiador.codigo_cliente = document.getElementById('fiador_codigo_cliente').value;
        fiador.numeroTelefono = document.getElementById('telefono2').value;
        fiador.lugar_trabajo = document.getElementById('lugar_trabajo').value;
        fiador.ingresos = document.getElementById('ingreso').value;
        //fiador.fotografia = document.getElementById('fotografiaF').files[0];


        addGuarantee('FIADOR', fiador.toJSON());
        clearFields();
        ocultar(document.getElementById('fiador'));
        document.getElementById('tipo_garantia').value = 0;
    });

}
