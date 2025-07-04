export class Coordenada{
    #longitud;
    #latitud;
    #address_id;

    constructor(latitud = '', longitud='', address_id = ''){
        this.#latitud = latitud;
        this.#longitud = longitud;
        this.#address_id = address_id;
    }

    // Getters
    get latitud(){
        return this.#latitud;
    }

    get longitud(){
        return this.#longitud;
    }

    get address_id(){
        return this.#address_id;
    }

    // Setters
    set latitud(value){
        if(!value || value.trim() === ''){
            alert('Debe de ingresar el registro de latitud de direccion');
            throw new Error('Debe de ingresar el registro de latitud de direccion')
        }
        this.#latitud = value.trim();
    }

    set longitud(value){
        if(!value || value.trim() === ''){
            alert('Debe de ingresar el registro de longitud de direccion');
            throw new Error('Debe de ingresar el registro de longitud de direccion')
        }
        this.#longitud = value.trim();
    }

    set address_id(value){        
        this.#address_id = value;
    }
    // Metodo para validar que todos los campos esten ingresados
    validar(){
        if(
            (this.#longitud.trim() ==='' &&  this.#latitud.trim() ==='' )||
            (!this.#longitud &&  !this.#latitud )
        ){
            return false;
        }
        return true;

    }

    // ToJson
    toJSON(){
        return {
            latitud:this.#latitud,
            longitud:this.#longitud,
            address_id:this.#address_id
        };
    }
    // ToString
    toString(){
        return `Coordinadas{
            latitud: ${this.#latitud},
            longitud:${this.#longitud},
            address_id:${this.#address_id}
        }`;
    }
}

// EXPORTAR LA CLASE
export default Coordenada;