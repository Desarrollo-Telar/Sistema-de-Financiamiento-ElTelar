import { DerechoDePosesionHipoteca } from '../../class/type_guarantee.js';

import { ocultar } from './ocultar_mostrar.js'
import { clearFields } from './limpiador.js'

// Evento para agregar una hipoteca
export function agregar_derecho_posesion(addGuarantee) {
    // Evento para agregar un Derecho de posesion hipoteca
    document.getElementById('agregar_garantiaDH').addEventListener('click', function (event) {
        event.preventDefault();

        let valor_cobertura = document.getElementById('valor_cobertura').value;
        if (!valor_cobertura || valor_cobertura === '') {
            alert('DEBE DE INGRESAR EL VALOR DE COBERTURA');
            return; // Cambiado para evitar el uso de `throw` en un evento DOM
        }

        const dh = new DerechoDePosesionHipoteca();
        const formData = new FormData();
        formData.append('noEscritura', document.getElementById('noEscritura1').value|| 0);
        formData.append('notario', document.getElementById('notario1').value|| 0);
        formData.append('area', document.getElementById('area1').value|| 0);
        formData.append('ubicacion', document.getElementById('ubicacion1').value|| 0);
        formData.append('descripcion', document.getElementById('descripcion1').value|| 0);
        formData.append('valor_comercial', document.getElementById('valor_comercial1').value|| 0);
        formData.append('titular', document.getElementById('titular1').value|| 0);
        formData.append('estatus', document.getElementById('estatus1').value|| 0);
        formData.append('noContratoArrendamiento', document.getElementById('noContratoArrendamiento1').value|| 0);
        //formData.append('avaluoBien', document.getElementById('avaluoBien1').files[0]|| 0);
        //formData.append('docDigitalSoporte', document.getElementById('docDigitalSoporte1').files[0]|| 0);


        dh.noEscritura = document.getElementById('noEscritura1').value;
        dh.notario = document.getElementById('notario1').value;
        dh.area = document.getElementById('area1').value;
        dh.ubicacion = document.getElementById('ubicacion1').value;
        dh.descripcion = document.getElementById('descripcion1').value;
        dh.valor_comercial = document.getElementById('valor_comercial1').value;
        dh.titular = document.getElementById('titular1').value;
        dh.estatus = document.getElementById('estatus1').value;
        dh.noContratoArrendamiento = document.getElementById('noContratoArrendamiento1').value;
        //dh.avaluoBien = document.getElementById('avaluoBien1').files[0];
        //dh.docDigitalSoporte = document.getElementById('docDigitalSoporte1').files[0];

        addGuarantee('DERECHO DE POSESION HIPOTECA', dh.toJSON(),formData);
        clearFields();
        ocultar(document.getElementById('derecho_posesion'));
        document.getElementById('tipo_garantia').value = 0;

    });


}
