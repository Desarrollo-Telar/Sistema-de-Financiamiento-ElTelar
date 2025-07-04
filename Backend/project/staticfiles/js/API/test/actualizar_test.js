
// Manejador de alertas
import {alerta_m} from '../../alertas/alertas.js'

// API PATCH
import {actualizar_credito} from '../credito/actualizar.js'

document.getElementById('test_actualizacion').addEventListener('submit', async function (event) {
    event.preventDefault();
    try{
        const formData = new FormData();
        formData.append('proposito', 'TEST DE API PATCH')
        await actualizar_credito(5,formData);
        alerta_m('Registro Completado',true);


    }catch (error){
        alerta_m(`${error}`)

    }
});