import { Cheque } from '../../class/type_guarantee.js';

import { ocultar } from './ocultar_mostrar.js'
import { clearFields } from './limpiador.js'

// Evento para agregar una hipoteca
export function agregar_cheque(addGuarantee) {
    // Evento para agregar un cheque
    document.getElementById('agregar_garantiaC').addEventListener('click', function (event) {
        event.preventDefault();

        let valor_cobertura = document.getElementById('valor_cobertura').value;
        if (!valor_cobertura || valor_cobertura === '') {
            alert('DEBE DE INGRESAR EL VALOR DE COBERTURA');
            return; // Cambiado para evitar el uso de `throw` en un evento DOM
        }

        const cheque = new Cheque();

        const formData = new FormData();
        formData.append('noCheque', document.getElementById('noCheque').value|| 0);
        formData.append('nombreCuenta', document.getElementById('nombreCuenta').value|| 0);
        formData.append('banco', document.getElementById('banco').value|| 0);
        formData.append('cheque_girado_a', document.getElementById('cheque_girado_a').value|| 0);
        formData.append('monto_cheque', document.getElementById('monto_cheque').value|| 0);
        //formData.append('fotografia_cheque', document.getElementById('cheque').files[0]);

        cheque.noCheque = document.getElementById('noCheque').value|| 0;
        cheque.nombreCuenta = document.getElementById('nombreCuenta').value|| 0;
        cheque.banco = document.getElementById('banco').value|| 0;
        cheque.cheque_girado_a = document.getElementById('cheque_girado_a').value|| 0;
        cheque.monto_cheque = document.getElementById('monto_cheque').value|| 0;
        //cheque.fotografia_cheque = document.getElementById('cheque').value || 0;

        addGuarantee('CHEQUE / PAGARE', cheque.toJSON(),formData);
        clearFields();
        ocultar(document.getElementById('cheque'));
        document.getElementById('tipo_garantia').value = 0;
    });

}
