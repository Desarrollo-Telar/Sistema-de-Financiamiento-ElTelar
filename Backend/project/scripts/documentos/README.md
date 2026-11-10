# Generador de Documentos Word (.docx) - El Telar S.A.

Esta carpeta (`scripts/documentos/`) contiene los módulos en Python para la generación automática y descarga de documentos legales formales en formato Word (`.docx`), como **Pagarés Libres de Protesto** y **Contratos de Reconocimiento de Deuda** (tanto para deudores individuales directos como con fiadores solidarios).

---

## 📁 Estructura del Módulo

```text
scripts/documentos/
├── __init__.py                     # Exportaciones públicas de funciones y utilidades
├── helpers.py                      # Formateadores legales (números a letras, CUI/DPI con espacios, NIT, cuentas, fechas notariales)
├── pagare.py                       # Generador de PAGARÉ LIBRE DE PROTESTO (Mario Antonio Chen Caal)
├── contrato_deudor_directo.py      # Generador de CONTRATO DE RECONOCIMIENTO DE DEUDA - DIRECTO (Candy Claramaría Cantoral)
├── contrato_con_fiador.py          # Generador de CONTRATO DE RECONOCIMIENTO DE DEUDA - CON FIADOR (Estefany Yusela & Fredy Joel)
├── contrato.py                     # Selector/dispatcher inteligente automático (con o sin fiador)
└── README.md                       # Documentación de uso y ejemplos
```

---

## 📄 Plantillas de Documentos Disponibles

### 1. Pagaré Libre de Protesto (`pagare.py`)
- **Partes:** Deudor, Acreedor (El Telar, S.A.), Avalista (opcional) y Notario.
- **Contenido:** Promesa incondicional de pago, términos y condiciones legales, cargos por atraso, orden de pagos, vencimiento anticipado, pactos procesales, firma del deudor, firma del avalista y acta notarial de legalización de firmas.

### 2. Contrato de Reconocimiento de Deuda - Deudor Directo (`contrato_deudor_directo.py`)
- **Partes (2 comparecientes):** Deudor individual y Representante Legal de El Telar S.A.
- **Cláusulas (3):**
  - **PRIMERA:** Reconocimiento de deuda lisa y llana, forma de pago con desglose mensual de cuotas, cuenta Banrural, destino del crédito, tasa de interés del 10% mensual, multa por mora del 10%, cesibilidad, vencimiento anticipado con título ejecutivo, renuncia al fuero de domicilio y **Garantía de Pago** (Mobiliaria sobre empresa mercantil o Laboral sobre sueldo institucional).
  - **SEGUNDA:** Aceptación expresa del Representante Legal.
  - **TERCERA:** Aceptación y ratificación de ambas partes.
- **Firmas:** 2 firmas (Deudora y Representante Legal) + Acta Notarial de Legalización de 2 firmas.

### 3. Contrato de Reconocimiento de Deuda - Con Fiador Solidario (`contrato_con_fiador.py`)
- **Partes (3 comparecientes):** Deudora, Fiador Solidario y Representante Legal de El Telar S.A.
- **Cláusulas (4):**
  - **PRIMERA:** Reconocimiento de deuda, desglose de pagos y fechas, cuenta bancaria, destino, tasa 10%, mora 10%, cesibilidad, vencimiento anticipado, renuncia de fuero de la deudora y **Garantía del Fiador** (constitución expresa como fiador solidario y mancomunado con garantía sobre empresa mercantil o sueldo institucional, fijando su dirección y renuncia de fuero).
  - **SEGUNDA:** Declaración de la deudora de haber sido plenamente instruida de las condiciones del crédito.
  - **TERCERA:** Aceptación expresa del Representante Legal.
  - **CUARTA:** Aceptación y ratificación de los tres comparecientes.
- **Firmas:** 3 firmas (Deudora, Fiador Solidario y Representante Legal) + Acta Notarial de Legalización de 3 firmas.

---

## 🚀 Uso en Python

```python
from scripts.documentos import (
    generar_pagare_word,
    generar_contrato_deudor_directo_word,
    generar_contrato_con_fiador_word,
    generar_contrato_word,
)

# 1. Pagaré Libre de Protesto
buf_pagare = generar_pagare_word()  # Retorna BytesIO
generar_pagare_word(output_target="pagare.docx")  # Guarda en archivo

# 2. Contrato Deudor Directo (Sin Fiador)
buf_directo = generar_contrato_deudor_directo_word()
generar_contrato_deudor_directo_word(output_target="contrato_directo.docx")

# 3. Contrato Con Fiador Solidario
buf_fiador = generar_contrato_con_fiador_word()
generar_contrato_con_fiador_word(output_target="contrato_fiador.docx")

# 4. Generador unificado automático:
# Detecta si se pasa fiador o no:
doc_directo = generar_contrato_word({"deudor_nombre": "Juan Pérez"})
doc_fiador = generar_contrato_word({"deudor_nombre": "Juan Pérez", "fiador_nombre": "Carlos Gómez"})
```

---

## 🌐 Enlaces de Descarga Web (Navegador)

Con el servidor Django corriendo (`python manage.py runserver` o Docker en el puerto 8000):

| Enlace / URL | Descripción |
| :--- | :--- |
| **`http://localhost:8000/documentos/`** | **Panel interactivo** con botones para descargar todos los documentos generados con un solo clic. |
| **`http://localhost:8000/documentos/pagare/ejemplo/`** | **Pagaré Libre de Protesto** (.docx) - Mario Antonio Chen Caal |
| **`http://localhost:8000/documentos/contrato/directo/ejemplo/`** | **Contrato Deudor Directo** (.docx) - Candy Claramaría Cantoral Caal |
| **`http://localhost:8000/documentos/contrato/fiador/ejemplo/`** | **Contrato con Fiador Solidario** (.docx) - Estefany Yusela López & Fredy Joel García |
| **`http://localhost:8000/documentos/pagare/<credit_id>/`** | Descarga de Pagaré desde un Crédito real de la base de datos |
