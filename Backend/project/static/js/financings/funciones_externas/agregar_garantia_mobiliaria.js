import { Mobiliaria } from '../../class/type_guarantee.js';

import { ocultar } from './ocultar_mostrar.js'
import { clearFields } from './limpiador.js'

// Evento para agregar una hipoteca
export function agregar_mobiliaria(addGuarantee) {
    // Evento para agregar un Mobiliaria
    document.getElementById('agregar_garantiaM').addEventListener('click', function (event) {
        event.preventDefault();

        let valor_cobertura = document.getElementById('valor_cobertura').value;
        if (!valor_cobertura || valor_cobertura === '') {
            alert('DEBE DE INGRESAR EL VALOR DE COBERTURA');
            return; // Cambiado para evitar el uso de `throw` en un evento DOM
        }
        const mobiliaria = new Mobiliaria();
        mobiliaria.descripcionBien = document.getElementById('descripcionBien').value;
        mobiliaria.documentoAcredita = document.getElementById('documentoAcredita1').value;
        //mobiliaria.imagenDocumentoAcredita = document.getElementById('imagenDocumentoAcredita').files[0];
        //mobiliaria.fotografiaBien = document.getElementById('fotografiaBien1').files[0];
        mobiliaria.noPoliza = document.getElementById('noPoliza1').value;
        mobiliaria.montoSeguro = document.getElementById('montoSeguro').value;




        addGuarantee('MOBILIARIA', mobiliaria.toJSON());
        clearFields();
        ocultar(document.getElementById('mobiliaria'));
        document.getElementById('tipo_garantia').value = 0;


    });
    

}
