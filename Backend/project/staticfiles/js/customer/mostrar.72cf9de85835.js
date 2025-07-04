

const mostrarOcultar = (id1, id2 = null, id3 = null) => {
    // Obtener los elementos por sus IDs
    let div = document.getElementById(id1);
    let div2 = id2 ? document.getElementById(id2) : null;
    let div3 = id3 ? document.getElementById(id3) : null;


    // Asegurarse de que el elemento principal exista antes de continuar
    if (!div) {
        console.error(`El elemento con id ${id1} no existe.`);
        return;
    }

    // Verificar si el elemento principal está visible
    if (window.getComputedStyle(div).display !== 'none') {
        // Ocultar el elemento principal
        ocultar(div);

        // Ocultar el tercer elemento si existe
        if (div3) {
            ocultar(div3);
        }

        // Mostrar el segundo elemento si existe
        if (div2) {
            mostrar(div2);
        }

        return false;
    }

    // Mostrar el elemento principal
    mostrar(div);

    // Ocultar el segundo elemento si existe
    if (div2) {
        ocultar(div2);
    }

    // Mostrar el tercer elemento si existe
    if (div3) {
        mostrar(div3);
    }
};


// Definición de las funciones mostrar y ocultar
const ocultar = (element) => {
    if (element) {
        element.style.display = 'none';
    }
};

const mostrar = (element) => {
    if (element) {
        element.style.display = 'block';
    }
};


const mostrarFuente = (id) => {
    let div = document.getElementById(id);
    let informacionLaborl = document.getElementById('informacionLaboral');
    let direccion = document.getElementById('direccion');
    let otra = document.getElementById('otra');


    if (div.value === 'Otra') {

        mostrar(otra);
        mostrar(direccion);
        ocultar(informacionLaborl);
    } else {

        mostrar(informacionLaborl);
        mostrar(direccion);
        ocultar(otra);

    }
}

let id_type_of_transfers_or_transfer_of_funds = document.getElementById('transferencias');

ocultar(id_type_of_transfers_or_transfer_of_funds);

document.addEventListener('DOMContentLoaded', (event) => {
    // Obtener el checkbox por su ID
    const checkbox = document.getElementById('transfers_or_transfer_of_funds');
    // Obtener el párrafo para mostrar el estado
    //const status = document.getElementById('id_type_of_transfers_or_transfer_of_funds');

    // Añadir un listener para el evento 'change'
    checkbox.addEventListener('change', (event) => {
        if (checkbox.checked) {
            //status.textContent = 'Checkbox is checked';

            mostrar(id_type_of_transfers_or_transfer_of_funds);
        } else {
            //status.textContent = 'Checkbox is unchecked';

            ocultar(id_type_of_transfers_or_transfer_of_funds);
        }
    });
});

// ------------------- MANEJO PARA SUBIR IMAGEN ------------------------
const imagen_mostrar = document.getElementById('imagen_mostrar');
const pdf_mostrar = document.getElementById('pdf_mostrar');
// AQUI ESTAN LOS INPUTS PARA SUBIR LOS DOCUMENTOS
const pdf_dpi = document.getElementById('pdf_dpi');
const imagenes_dpi = document.getElementById('imagenes_dpi');

imagen_mostrar.addEventListener('input',function (event){
    let on = event.target.value;
    if(on){
        mostrar(imagenes_dpi);
        ocultar(pdf_dpi);
    }

});

pdf_mostrar.addEventListener('input',function (event){
    let on = event.target.value;
    if(on){
        ocultar(imagenes_dpi);
        mostrar(pdf_dpi);
    }

});

var municipios = [
    // GUATEMALA
    {
        id:0,
        text: 'CIUDAD DE GUATEMALA'
    },
    {
        id:1,
        text: 'AMATITLÁN'
    },
    {
        id:2,
        text: 'CHINAUTLA'
    },
    {
        id:3,
        text: 'FRAIJANES'
    },
    {
        id:4,
        text: 'MIXCO'
    },
    {
        id:5,
        text: 'PALENCIA'
    },
    {
        id:6,
        text: 'SAN JOSÉ DEL GOLFO'
    },
    {
        id:7,
        text: 'SAN JOSÉ PINULA'
    },
    {
        id:8,
        text: 'SAN JUAN SACATEPÉQUEZ'
    },
    {
        id:9,
        text: 'SAN MIGUEL PETAPA'
    },
    {
        id:10,
        text: 'SAN PEDRO AYAMPUC'
    },
    {
        id:11,
        text: 'SAN PEDRO SACATEPÉQUEZ'
    },
    {
        id:12,
        text: 'SANTA CATARINA PINULA'
    },
    {
        id:13,
        text: 'VILLA CANALES'
    },
    {
        id:14,
        text: 'VILLA NUEVA'
    },
    // SACATEPÉQUEZ
    {
        id:15,
        text: 'ANTIGUA GUATEMALA'
    },
    {
        id:16,
        text: 'CIUDAD VIEJA'
    },
    {
        id:17,
        text: 'JOCOTENANGO'
    },
    {
        id:18,
        text: 'PARRAMOS'
    },
    {
        id:19,
        text: 'SAN ANTONIO AGUAS CALIENTES'
    },
    {
        id:20,
        text: 'SAN BARTOLOMÉ MILPAS ALTAS'
    },
    {
        id:21,
        text:'SAN LUCAS SACATEPÉQUEZ'
    },
    {
        id:22,
        text: 'SAN MIGUEL DUEÑAS'
    },
    {
        id:23,
        text: 'SANTA CATARINA BARAHONA'
    },
    {
        id:24,
        text: 'SANTA LUCÍA MILPAS ALTAS'
    },
    {
        id:25,
        text: 'SANTA MARÍA DE JESÚS'
    },
    {
        id:26,
        text: 'SANTIAGO SACATEPÉQUEZ'
    },
    {
        id:27,
        text: 'SANTO DOMINGO XENACOJ'
    },
    // CHIMALTENANGO
    {
        id:28,
        text: 'CHIMALTENANGO'
    },
    {
        id:29,
        text: 'ACATENANGO'
    },
    {
        id:30,
        text: 'COMALAPA'
    },
    {
        id:31,
        text: 'EL TEJAR'
    },
    {
        id:32,
        text: 'PARRAMOS'
    },
    {
        id:33,
        text: 'PATZICÍA'
    },
    {
        id:34,
        text: 'PATZÚN'
    },
    {
        id:35,
        text: 'POCHUTA'
    },
    {
        id:36,
        text: 'SAN ANDRÉS ITZAPA'
    },
    {
        id:37,
        text: 'SAN JOSÉ POAQUIL'
    },
    {
        id:38,
        text: 'SAN MARTÍN JILOTEPEQUE'
    },
    {
        id:39,
        text: 'SANTA APOLONIA'
    },
    {
        id:40,
        text: 'SANTA CRUZ BALANYÁ'
    },
    {
        id:41,
        text: 'TECPÁN'
    },
    {
        id:42,
        text: 'YEPACAPA'
    },
    {
        id:43,
        text: 'ZARAGOZA'
    },
    // ESCUINTLA
    {
        id:44,
        text: 'ESCUINTLA'
    },
    {
        id:45,
        text: 'LA DEMOCRACIA'
    },
    {
        id:46,
        text: 'MASAGUA'
    },
    {
        id:47,
        text: 'PALÍN'
    },
    {
        id:48,
        text: 'SAN JOSÉ'
    },
    {
        id:49,
        text: 'SAN VICENTE PACAYA'
    },
    {
        id:50,
        text: 'SANTA LUCÍA COTZUMALGUAPA'
    },
    {
        id:51,
        text: 'SIQUINALÁ'
    },
    {
        id:52,
        text: 'TIQUISATE'
    },
    // SANTA ROSA
    {
        id:53,
        text: 'CUILAPA'
    },
    {
        id:54,
        text: 'BARBERENA'
    },
    {
        id:55,
        text: 'CASILLAS'
    },
    {
        id:56,
        text: 'CHIQUIMULILLA'
    },
    {
        id:57,
        text: 'GUAZACAPÁN'
    },
    {
        id:58,
        text: 'NUEVA SANTA ROSA'
    },
    {
        id:59,
        text: 'ORATORIO'
    },
    {
        id:60,
        text: 'PUEBLO NUEVO VIÑAS'
    },
    {
        id:61,
        text: 'SAN JUAN TECUACO'
    },
    {
        id:62,
        text: 'SANTA CRUZ NARANJO'
    },
    {
        id:63,
        text: 'SANTA MARÍA IXHUATÁN'
    },
    {
        id:64,
        text: 'SANTA ROSA DE LIMA'
    },
    {
        id:65,
        text: 'TAXISCO'
    },
    // SOLOLÁ
    {
        id:66,
        text: 'SOLOLÁ'
    },
    {
        id:67,
        text: 'CONCEPCIÓN'
    },
    {
        id:68,
        text: 'NAHUALÁ'
    },
    {
        id:69,
        text: 'PANAJACHEL'
    },
    {
        id:70,
        text: 'SAN ANDRÉS SEMETABAJ'
    },
    {
        id:71,
        text: 'SAN ANDRÉS SEMETABAJ'
    },
    {
        id:72,
        text: 'SAN ANTONIO PALOPÓ'
    },
    {
        id:73,
        text: 'SAN JOSÉ CHACAYÁ'
    },
    {
        id:74,
        text: 'SAN JUAN LA LAGUNA'
    },{
        id:75,
        text: 'SAN LUCAS TOLIMÁN'
    },
    {
        id:76,
        text: 'SAN MARCOS LA LAGUNA'
    },
    {
        id:77,
        text: 'SAN PABLO LA LAGUNA'
    },
    {
        id:78,
        text: 'SAN PEDRO LA LAGUNA'
    },
    {
        id:79,
        text: 'SANTA CATARINA IXTAHUACÁN'
    },
    {
        id:80,
        text: 'SANTA CATARINA PALOPÓ'
    },
    {
        id:81,
        text: 'SANTA CLARA LA LAGUNA'
    },
    {
        id:82,
        text: 'SANTA CRUZ LA LAGUNA'
    },
    {
        id:83,
        text: 'SANTA LUCÍA UTATLÁN'
    },
    {
        id:84,
        text: 'SANTA MARÍA VISITACIÓN'
    },
    {
        id:85,
        text: 'SANTIAGO ATITLÁN'
    },
    // TOTONICAPÁN
    {
        id:86,
        text: 'TOTONICAPÁN'
    },
    {
        id:87,
        text: 'MOMOSTENANGO'
    },
    {
        id:88,
        text: 'SAN ANDRÉS XECUL'
    },
    {
        id:89,
        text: 'SAN BARTOLO'
    },
    {
        id:90,
        text: 'SAN CRISTÓBAL TOTONICAPÁN'
    },
    {
        id:91,
        text: 'SAN FRANCISCO EL ALTO'
    },
    {
        id:92,
        text: 'SANTA LUCÍA LA REFORMA'
    },
    {
        id:93,
        text: 'SANTA MARÍA CHIQUIMULA'
    },
    {
        id:94,
        text: 'SANTA MARÍA TOTONICAPÁN'
    },
    // QUETZALTENANGO
    {
        id:95,
        text: 'QUETZALTENANGO'
    },
    {
        id:96,
        text: 'ALMOLONGA'
    },
    {
        id:97,
        text: 'CANTEL'
    },
    {
        id:98,
        text: 'COATEPEQUE'
    },
    {
        id:99,
        text: 'COLOMBA'
    },
    {
        id:100,
        text: 'CONCEPCIÓN CHIQUIRICHAPA'
    },
    {
        id:101,
        text: 'EL PALMAR'
    },
    {
        id:102,
        text: 'FLORES COSTA CUCA'
    },
    {
        id:103,
        text: 'LA ESPERANZA'
    },
    {
        id:104,
        text: 'OLINTEPEQUE'
    },
    {
        id:105,
        text: 'PALESTINA DE LOS ALTOS'
    },
    {
        id:106,
        text: 'SALCAJÁ'
    },
    {
        id:107,
        text: 'SAN CARLOS SIJA'
    },
    {
        id:108,
        text: 'SAN FRANCISCO LA UNIÓN'
    },
    {
        id:109,
        text: 'SAN JUAN OSTUNCALCO'
    },
    {
        id:110,
        text: 'SAN MARTÍN SACATEPÉQUEZ'
    },
    {
        id:111,
        text: 'SAN MATEO'
    },
    {
        id:112,
        text: 'SAN MIGUEL SIGÜILÁ'
    },
    {
        id:113,
        text: 'SIBILIA'
    },
    {
        id:114,
        text: 'ZUNIL'
    },
    // SUCHITEPÉQUEZ
    {
        id:115,
        text: 'MAZATENANGO'
    },
    {
        id:116,
        text: 'CHICACAO'
    },
    {
        id:117,
        text: 'CUYOTENANGO'
    },
    {
        id:118,
        text: 'PATULUL'
    },
    {
        id:119,
        text: 'PUEBLO NUEVO'
    },
    {
        id:120,
        text: 'RÍO BRAVO'
    },
    {
        id:121,
        text: 'SAMAYAC'
    },
    {
        id:122,
        text: 'SAN ANTONIO SUCHITEPÉQUEZ'
    },
    {
        id:123,
        text: 'SAN BERNARDINO'
    },
    {
        id:124,
        text: 'SAN FRANCISCO ZAPOTITLÁN'
    },

    {
        id:125,
        text: 'SAN GABRIEL'
    },
    {
        id:126,
        text: 'SAN JOSÉ EL ÍDOLO'
    },
    {
        id:127,
        text: 'SAN JOSÉ LA MÁQUINA'
    },
    {
        id:128,
        text: 'SAN JUAN BAUTISTA'
    },
    {
        id:129,
        text: 'SAN LORENZO'
    },
    {
        id:130,
        text: 'SAN MIGUEL PANÁN'
    },

    {
        id:131,
        text: 'SAN PABLO JOCOPILAS'
    },
    {
        id:132,
        text: 'SANTA BÁRBARA'
    },
    {
        id:133,
        text: 'SANTO DOMINGO SUCHITEPEQUEZ'
    },
    {
        id:134,
        text: 'SANTO TOMÁS LA UNIÓN'
    },
    {
        id:135,
        text: 'ZUNILITO'
    },
    // RETALHULEU
    {
        id:136,
        text: 'RETALHULEU'
    },
    {
        id:137,
        text: 'CHAMPERICO'
    },
    {
        id:138,
        text: 'EL ASINTAL'
    },
    {
        id:139,
        text: 'NUEVO SAN CARLOS'
    },
    {
        id:140,
        text: 'SAN ANDRÉS VILLA SECA'
    },
    {
        id:141,
        text: 'SAN FELIPE'
    },
    {
        id:142,
        text: 'SAN MARTÍN ZAPOTITLÁN'
    },
    {
        id:143,
        text: 'SANTA CRUZ MULUÁ'
    },
    {
        id:144,
        text: 'SANTA ROSA'
    },
    {
        id:145,
        text: 'TULATE'
    },
    // SAN MARCOS
    {
        id:146,
        text: 'SAN MARCOS'
    },
    {
        id:147,
        text: 'AYUTLA'
    },
    {
        id:148,
        text: 'CATARINA'
    },
    {
        id:149,
        text: 'COMITANCILLO'
    },
    {
        id:150,
        text: 'CONCEPCIÓN TUTUAPA'
    },
    {
        id:151,
        text: 'EL QUETZAL'
    },
    {
        id:152,
        text: 'EL RODEO'
    },
    {
        id:153,
        text: 'EL TUMBADOR'
    },
    {
        id:154,
        text: 'ESQUIPULAS PALO GORDO'
    },
    {
        id:155,
        text: 'IXCHIGUAN'
    },
    {
        id:156,
        text: 'LA REFORMA'
    },
    {
        id:157,
        text: 'MALACATÁN'
    },
    {
        id:158,
        text: 'NUEVO PROGRESO'
    },
    {
        id:159,
        text: 'OCÓS'
    },
    {
        id:160,
        text: 'RÍO BLANCO'
    },
    {
        id:161,
        text: 'SAN ANTONIO SACATEPÉQUEZ'
    },
    {
        id:162,
        text: 'SAN CRISTÓBAL CUCHO'
    },
    {
        id:163,
        text: 'SAN JOSÉ EL RODEO'
    },
    {
        id:164,
        text: 'SAN LORENZO'
    },
    {
        id:165,
        text: 'SAN MIGUEL IXTAHUACÁN'
    },
    {
        id:166,
        text: 'SAN PABLO'
    },
    {
        id:167,
        text: 'SAN PEDRO SACATEPÉQUEZ'
    },
    {
        id:168,
        text: 'SAN RAFAEL PIE DE LA CUESTA'
    },
    {
        id:169,
        text: 'SIBINAL'
    },
    {
        id:170,
        text: 'SIPACAPA'
    },
    {
        id:171,
        text: 'TACANÁ'
    },
    {
        id:172,
        text: 'TAJUMULCO'
    },
    // HUEHUETENANGO
    {
        id:173,
        text: 'HUEHUETENANGO'
    },
    {
        id:174,
        text: 'AGUACATÁN'
    },
    {
        id:175,
        text: 'CHIANTLA'
    },
    {
        id:176,
        text: 'COLOTENANGO'
    },
    {
        id:177,
        text: 'CONCEPCIÓN HUISTA'
    },
    {
        id:178,
        text: 'CUILCO'
    },
    {
        id:179,
        text: 'HUEHUETENANGO'
    },
    {
        id:180,
        text: 'JACALTENANGO'
    },
    {
        id:181,
        text: 'LA DEMOCRACIA'
    },
    {
        id:182,
        text: 'LA LIBERTAD'
    },
    {
        id:183,
        text: 'MALACATANCITO'
    },
    {
        id:184,
        text: 'NENTÓN'
    },
    {
        id:185,
        text: 'SAN ANTONIO HUISTA'
    },
    {
        id:186,
        text: 'SAN GASPAR IXCHIL'
    },
    {
        id:187,
        text: 'SAN ILDEFONSO IXTAHUACÁN'
    },
    {
        id:188,
        text: 'SAN JUAN ATITÁN'
    },
    {
        id:189,
        text: 'SAN JUAN IXCOY'
    },
    {
        id:190,
        text: 'SAN MATEO IXTATÁN'
    },
    {
        id:191,
        text: 'SAN MIGUEL ACATÁN'
    },
    {
        id:192,
        text: 'SAN PEDRO NECTA'
    },
    {
        id:193,
        text: 'SAN PEDRO SOLÓMA'
    },
    {
        id:194,
        text: 'SAN RAFAEL LA INDEPENDENCIA'
    },
    {
        id:195,
        text: 'SAN RAFAEL PETZAL'
    },
    {
        id:196,
        text: 'SAN SEBASTIÁN COATÁN'
    },
    {
        id:197,
        text: 'SAN SEBASTIÁN HUEHUETENANGO'
    },
    {
        id:198,
        text: 'SANTA ANA HUISTA'
    },
    {
        id:199,
        text: 'SANTA BÁRBARA'
    },
    {
        id:200,
        text: 'SANTA EULALIA'
    },
    {
        id:201,
        text: 'SANTIAGO CHIMALTENANGO'
    },
    {
        id:202,
        text: 'TECTITÁN'
    },
    {
        id:203,
        text: 'TODOS SANTOS CUCHUMATÁN'
    },
    // QUICHE
    {
        id:204,
        text: 'SANTA CRUZ DEL QUICHÉ'
    },
    {
        id:205,
        text: "AK' TENAMIT"
    },
    {
        id:206,
        text: 'CANILLÁ'
    },
    {
        id:207,
        text: 'CHAJUL'
    },
    {
        id:208,
        text: 'CHICAMÁN'
    },
    {
        id:209,
        text: 'CHICHÉ'
    },
    {
        id:210,
        text: 'CHICHICASTENANGO'
    },
    {
        id:211,
        text: 'CHINIQUE'
    },
    {
        id:212,
        text: 'CUNÉN'
    },
    {
        id:213,
        text: 'IXCÁN'
    },
    {
        id:214,
        text: 'JOYABAJ'
    },
    {
        id:215,
        text: 'NEBAJ'
    },
    {
        id:216,
        text: 'PACHALUM'
    },
    {
        id:217,
        text: 'PATZITÉ'
    },
    {
        id:218,
        text: 'SACAPULAS'
    },
    {
        id:219,
        text: 'SAN ANDRÉS SAJCABAJÁ'
    },
    {
        id:220,
        text: 'SAN ANTONIO ILOTENANGO'
    },
    {
        id:221,
        text: 'SAN BARTOLOMÉ JOCOTENANGO'
    },
    {
        id:222,
        text: 'SAN JUAN COTZAL'
    },
    {
        id:223,
        text: 'SAN PEDRO JOCOPILAS'
    },
    {
        id:224,
        text: 'SANTA CR'
    },
    // BAJA VERAPAZ
    {
        id:225,
        text: 'SALAMÁ'
    },
    {
        id:226,
        text: 'CUBULCO'
    },

    {
        id:227,
        text: 'GRANADOS'
    },
    {
        id:228,
        text: 'PURULHÁ'
    },
    {
        id:229,
        text: 'RABINAL'
    },
    {
        id:230,
        text: 'SAN JERÓNIMO'
    },
    {
        id:231,
        text: 'SAN MIGUEL CHICAJ'
    },
    // ALTA VERAPAZ
    {
        id:232,
        text: 'COBÁN'
    },
    {
        id:233,
        text: 'CAHABÓN'
    },
    {
        id:234,
        text: 'CHAHAL'
    },
    {
        id:235,
        text: 'CHISEC'
    },
    {
        id:236,
        text: 'FRAY BARTOLOMÉ DE LAS CASAS'
    },
    {
        id:237,
        text: 'LANQUÍN'
    },
    {
        id:238,
        text: 'PANZÓS'
    },
    {
        id:239,
        text: 'SAN CRISTÓBAL VERAPAZ'
    },
    {
        id:240,
        text: 'SAN JUAN CHAMELCO'
    },
    {
        id:241,
        text: 'SAN PEDRO CARCHÁ'
    },
    {
        id:242,
        text: 'SANTA CATALINA LA TINTA'
    },
    {
        id:243,
        text: 'SANTA CRUZ VERAPAZ'
    },
    {
        id:244,
        text: 'SENAHÚ'
    },
    {
        id:245,
        text: 'TACTIC'
    },
    {
        id:246,
        text: 'TAMAHÚ'
    },
    // PETEN
    {
        id:247,
        text: 'FLORES'
    },
    {
        id:248,
        text: 'DOLORES'
    },
    {
        id:249,
        text: 'LA LIBERTAD'
    },
    {
        id:250,
        text: 'MELCHOR DE MENCOS'
    },
    {
        id:251,
        text: 'POPTÚN'
    },
    {
        id:252,
        text: 'SAN ANDRÉS'
    },
    {
        id:253,
        text: 'SAN BENITO'
    },
    {
        id:254,
        text: 'SAN FRANCISCO'
    },
    {
        id:255,
        text: 'SAN JOSÉ'
    },
    {
        id:256,
        text: 'SAN LUIS'
    },
    {
        id:257,
        text: 'SANTA ANA'
    },
    {
        id:258,
        text: 'SAYAXCHÉ'
    },
    // IZABAL
    {
        id:259,
        text: 'PUERTO BARRIOS'
    },
    {
        id:260,
        text: 'EL ESTOR'
    },
    {
        id:261,
        text: 'LIVINGSTON'
    },
    {
        id:262,
        text: 'LOS AMATES'
    },
    {
        id:263,
        text: 'MORALES'
    },
    // ZACAPA
    {
        id:264,
        text: 'ZACAPA'
    },
    {
        id:265,
        text: 'CABAÑAS'
    },
    {
        id:266,
        text: 'ESTANZUELA'
    },
    {
        id:267,
        text: 'GUALÁN'
    },
    {
        id:268,
        text: 'HUITÉ'
    },
    {
        id:269,
        text: 'LA UNIÓN'
    },
    {
        id:270,
        text: 'RÍO HONDO'
    },
    {
        id:271,
        text: 'SAN DIEGO'
    },
    {
        id:272,
        text: 'SANTA LUCÍA LA REFORMA'
    },
    {
        id:273,
        text: 'USUMATLÁN'
    },
    // CHIQUIMULA
    {
        id:274,
        text: 'CHIQUIMULA'
    },
    {
        id:275,
        text: 'CAMOTÁN'
    },
    {
        id:276,
        text: 'CONCEPCIÓN LAS MINAS'
    },
    {
        id:277,
        text: 'ESQUIPULAS'
    },
    {
        id:278,
        text: 'IPALA'
    },
    {
        id:279,
        text: 'JOCOTÁN'
    },
    {
        id:280,
        text: 'OLOPA'
    },
    {
        id:281,
        text: 'QUEZALTEPEQUE'
    },
    {
        id:282,
        text: 'SAN JACINTO'
    },
    {
        id:283,
        text: 'SAN JOSÉ LA ARADA'
    },
    // JALAPA
    {
        id:284,
        text: 'JALAPA'
    },
    {
        id:285,
        text: 'SAN PEDRO PINULA'
    },
    {
        id:286,
        text: 'MATAQUESCUINTLA'
    },
    {
        id:287,
        text: 'MONJAS'
    },
    // JUTIAPA
    {
        id:288,
        text: 'JUTIAPA'
    },
    {
        id:289,
        text: 'ASUNCIÓN MITA'
    },
    {
        id:290,
        text: 'JALPATAGUA'
    },
    {
        id:291,
        text: 'SANTA CATARINA MITA'
    },
    // EL PROGRESO
    {
        id:292,
        text: 'GUASTATOYA'
    },

    {
        id:293,
        text: 'SANARATE'
    },
    {
        id:294,
        text: 'EL JÍCARO'
    },
    {
        id:295,
        text: 'SANSARE'
    }
]

var departamentos = [
    {
        id:0,
        text: 'GUATEMALA'
    },
    {
        id:1,
        text: 'SACATEPÉQUEZ'
    },
    {
        id:2,
        text: 'CHIMALTENANGO'
    },
    {
        id:3,
        text: 'ESCUINTLA'
    },
    {
        id:4,
        text: 'SANTA ROSA'
    },
    {
        id:5,
        text: 'SOLOLÁ'
    },
    {
        id:6,
        text: 'TOTONICAPÁN'
    },
    {
        id:7,
        text: 'QUETZALTENANGO'
    },
    {
        id:8,
        text: 'SUCHITEPÉQUEZ'
    },
    {
        id:9,
        text: 'RETALHULEU'
    },
    {
        id:10,
        text: 'SAN MARCOS'
    },
    {
        id:11,
        text: 'HUEHUETENANGO'
    },
    {
        id:12,
        text: 'QUICHÉ'
    },
    {
        id:13,
        text: 'BAJA VERAPAZ'
    },
    {
        id:14,
        text: 'ALTA VERAPAZ'
    },
    {
        id:15,
        text: 'PETÉN'
    },
    {
        id:16,
        text: 'IZABAL'
    },
    {
        id:17,
        text: 'ZACAPA'
    },
    {
        id:18,
        text: 'CHIQUIMULA'
    },
    {
        id:19,
        text: 'JALAPA'
    },
    {
        id:20,
        text: 'JUTIAPA'
    },
    {
        id:21,
        text: 'EL PROGRESO'
    },
]

$(document).ready(function() {
    
    $(".city1").select2({
        data: departamentos
    });
    $(".state1").select2({
        data: municipios
    });
    $(".city2").select2({
        data: departamentos
    });
    $(".state2").select2({
        data: municipios
    });
    
   
    
    
});