
import { urls_p } from '../../API/urls_api.js'

document.getElementById('cuota_por_cobrar').addEventListener('click', () => {
    const id_credito = document.getElementById('credit_id').value;
    
    let resultado = fetchLastPaymentPlan(id_credito);
    console.log(resultado);
});

function formato_fechas(fecha) {
    const date = new Date(fecha);

    // Extraer día, mes y año
    const day = String(date.getDate()).padStart(2, '0'); // Asegura dos dígitos
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Meses empiezan desde 0
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;

}
async function fetchLastPaymentPlan(searchTerm) {
    try {
        // URL del endpoint con el parámetro 'term'
        const url = `${urls_p.api_url_cuota}?term=${encodeURIComponent(searchTerm)}`;

        // Realizar la solicitud GET con Axios
        const response = await axios.get(url);

        // Procesar la respuesta
        if (response.data) {
            //console.log('Último PaymentPlan:', response.data);
            console.log(response.data['credit_id'].is_paid_off);

            if (response.data['credit_id'].is_paid_off){
                Swal.fire({
                    title: "Este Credito ya ha sido cancelado por completo",
                   
                    icon: "info",
    
                });

            }else{
                Swal.fire({
                    title: "Cuota por Cobrar:",
                    html: `<p>Fecha de Inicio: ${formato_fechas(response.data['start_date'])} </p>
                <p>Fecha de Vencimiento:  ${formato_fechas(response.data['due_date'])} </p>
                <p>Fecha Limite:  ${formato_fechas(response.data['fecha_limite'])} </p>
                <p>Mora: Q${response.data['mora']}</p>
                <p>Interes: Q${response.data['interest']}</p>
                <p>Total de la Cuota a Cancelar: Q${response.data['total_cancelar']}</p>
                           
                `,
                    icon: "info",
    
                });

            }

            
            

        } else {
            console.log('No se encontraron datos para el término de búsqueda:', searchTerm);
        }
    } catch (error) {
        console.error('Error al buscar el PaymentPlan:', error.response || error.message);
        return error;
    }
}