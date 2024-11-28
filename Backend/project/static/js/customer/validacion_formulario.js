
import { Cliente } from '../class/customer.js'

//output_name_customer
const first_name = document.getElementById('first_name');
const last_name = document.getElementById('last_name');


function updateOutput() {
    const output_name_customer = document.getElementById('output_name_customer');
    const workingInformation = document.getElementById('output_info_name_customer');
    const plan = document.getElementById('output_plan_name_customer');
    const refe = document.getElementById('output_refe_name_customer');
    const image = document.getElementById('output_image_name_customer');
    output_name_customer.textContent = `CLIENTE: ${first_name.value} ${last_name.value}`.trim();
    workingInformation.textContent =  `CLIENTE: ${first_name.value} ${last_name.value}`.trim();
    plan.textContent =  `CLIENTE: ${first_name.value} ${last_name.value}`.trim();
    refe.textContent =  `CLIENTE: ${first_name.value} ${last_name.value}`.trim();
    image.textContent =  `CLIENTE: ${first_name.value} ${last_name.value}`.trim();
}

first_name.addEventListener('input', updateOutput);
last_name.addEventListener('input', updateOutput);

