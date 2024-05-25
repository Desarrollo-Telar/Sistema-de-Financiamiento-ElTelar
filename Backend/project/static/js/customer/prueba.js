
import Cliente from '../class/customer.js';
import Direccion from '../class/address.js';
import PlanInversion from '../class/investmentplan.js';
import OtraInformacionLaboral from '../class/othersourcesofincome.js';
import Referencia from '../class/reference.js';
import InformacionLaboral from '../class/workinginformation.js';

let cliente = new Cliente();
let direccion = [
    new Direccion(),
    new Direccion(),
];
let planInversion = new PlanInversion();
let otraInformacionLaboral = new OtraInformacionLaboral();
let referencia = [
    new Referencia(),
    new Referencia(),
    new Referencia(),
    new Referencia(),
];
let informacionLaboral = new InformacionLaboral();