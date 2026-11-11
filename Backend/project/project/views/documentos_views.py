"""
Vistas para la descarga y generación de documentos Word (.docx)
(Pagaré Libre de Protesto, Contratos de Reconocimiento de Deuda con/sin fiador, etc.)
para El Telar S.A.
"""

from urllib.parse import quote
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from scripts.documentos import (
    generar_pagare_word,
    generar_pagare_desde_credito,
    obtener_datos_ejemplo,
    generar_contrato_word,
    obtener_datos_ejemplo_contrato,
    generar_contrato_deudor_directo_word,
    generar_contrato_deudor_directo_desde_solicitud,
    extraer_datos_contrato_deudor_directo_desde_solicitud,
    obtener_datos_ejemplo_deudor_directo,
    generar_contrato_con_fiador_word,
    generar_contrato_con_fiador_desde_solicitud,
    extraer_datos_contrato_con_fiador_desde_solicitud,
    obtener_datos_ejemplo_con_fiador,
)

# MIME type oficial para archivos Microsoft Word .docx
DOCX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def _resolver_objeto_credito_o_404(credit_id):
    """
    Resuelve primero desde InvestmentPlan (solicitud) y, como respaldo, desde Credit.
    Lanza Http404 si ninguno existe.
    """
    credito = None
    try:
        from apps.InvestmentPlan.models import InvestmentPlan
        credito = (
            InvestmentPlan.objects
            .select_related("customer_id", "sucursal", "asesor_responsable")
            .filter(id=credit_id)
            .first()
        )
    except ImportError:
        credito = None

    if credito is not None:
        return credito

    try:
        from apps.financings.models import Credit
        return get_object_or_404(
            Credit.objects.select_related("customer_id", "sucursal", "destino_id"),
            id=credit_id,
        )
    except Exception:
        raise Http404("No se encontró la solicitud de inversión o crédito especificado.")


@require_GET
def descargar_pagare_ejemplo(request):
    """
    Genera y descarga el archivo Word (.docx) del Pagaré de Ejemplo.
    Permite además sobrescribir parámetros dinámicamente mediante query params en la URL:
    Ejemplo: /documentos/pagare/ejemplo/?deudor=Juan+Perez&monto=50000&plazo=6&dpi=1234567890101
    """
    datos = obtener_datos_ejemplo()

    if request.GET.get("deudor"):
        datos["deudor_nombre"] = request.GET.get("deudor")
        datos["aval_persona_avalada"] = request.GET.get("deudor")
    if request.GET.get("monto"):
        try:
            datos["capital_adeudado"] = float(request.GET.get("monto"))
            datos["aval_monto"] = datos["capital_adeudado"]
        except ValueError:
            pass
    if request.GET.get("plazo"):
        try:
            datos["plazo_meses"] = int(request.GET.get("plazo"))
            datos["numero_cuotas"] = datos["plazo_meses"]
        except ValueError:
            pass
    if request.GET.get("dpi"):
        datos["deudor_dpi"] = request.GET.get("dpi")
    if request.GET.get("nit"):
        datos["deudor_nit"] = request.GET.get("nit")
    if request.GET.get("tasa"):
        try:
            datos["tasa_interes"] = float(request.GET.get("tasa"))
        except ValueError:
            pass
    if request.GET.get("vencimiento"):
        datos["fecha_vencimiento"] = request.GET.get("vencimiento")

    buffer = generar_pagare_word(datos)

    nombre_archivo = f"pagare_{datos.get('deudor_nombre', 'ejemplo').replace(' ', '_').lower()}.docx"
    response = HttpResponse(buffer.getvalue(), content_type=DOCX_MIME_TYPE)
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
    response["Content-Length"] = len(buffer.getvalue())
    return response


@require_GET
def descargar_pagare_credito(request, credit_id):
    """
    Genera y descarga el Pagaré Word (.docx) vinculado a una Solicitud (InvestmentPlan) o Crédito real en el sistema.
    """
    try:
        from apps.InvestmentPlan.models import InvestmentPlan
        credito = InvestmentPlan.objects.filter(id=credit_id).first()
    except ImportError:
        credito = None

    if not credito:
        try:
            from apps.financings.models import Credit
            credito = get_object_or_404(Credit, id=credit_id)
        except Exception:
            raise Http404("No se encontró la solicitud de inversión o crédito especificado.")

    buffer = generar_pagare_desde_credito(credito)

    codigo = getattr(credito, 'investment_plan_code', None) or getattr(credito, 'codigo_credito', None) or f"id_{credito.id}"
    nombre_archivo = f"pagare_credito_{codigo}.docx"

    response = HttpResponse(buffer.getvalue(), content_type=DOCX_MIME_TYPE)
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
    response["Content-Length"] = len(buffer.getvalue())
    return response


@require_GET
def descargar_contrato_directo_ejemplo(request):
    """
    Genera y descarga el Contrato de Reconocimiento de Deuda para Deudor Directo (sin fiador).
    Plantilla: Candy Claramaría Cantoral Caal de Papa.
    """
    datos = obtener_datos_ejemplo_deudor_directo()
    if request.GET.get("deudor"):
        datos["deudor_nombre"] = request.GET.get("deudor")
    if request.GET.get("monto"):
        try:
            datos["monto_capital"] = float(request.GET.get("monto"))
        except ValueError:
            pass

    buffer = generar_contrato_deudor_directo_word(datos)
    nombre_archivo = "contrato_reconocimiento_deudor_directo.docx"
    response = HttpResponse(buffer.getvalue(), content_type=DOCX_MIME_TYPE)
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
    response["Content-Length"] = len(buffer.getvalue())
    return response


@require_GET
def descargar_contrato_fiador_ejemplo(request):
    """
    Genera y descarga el Contrato de Reconocimiento de Deuda Con Fiador(es) Solidario(s).
    Soporta dinámicamente cualquier número de fiadores (ej. ?num_fiadores=3 o ?num_fiadores=5).
    """
    num_f = 1
    if request.GET.get("num_fiadores"):
        try:
            num_f = int(request.GET.get("num_fiadores"))
        except ValueError:
            num_f = 1
    elif request.GET.get("fiadores") and request.GET.get("fiadores").isdigit():
        num_f = int(request.GET.get("fiadores"))

    datos = obtener_datos_ejemplo_con_fiador(cantidad_fiadores=num_f)
    if request.GET.get("deudor"):
        datos["deudor_nombre"] = request.GET.get("deudor")
    if request.GET.get("fiador") and len(datos["fiadores"]) > 0:
        datos["fiadores"][0]["nombre"] = request.GET.get("fiador")
        datos["fiador_nombre"] = request.GET.get("fiador")
    if request.GET.get("monto"):
        try:
            datos["monto_capital"] = float(request.GET.get("monto"))
        except ValueError:
            pass

    buffer = generar_contrato_con_fiador_word(datos)
    sufijo = f"con_{len(datos['fiadores'])}_fiadores" if len(datos['fiadores']) > 1 else "con_fiador"
    nombre_archivo = f"contrato_reconocimiento_{sufijo}.docx"
    response = HttpResponse(buffer.getvalue(), content_type=DOCX_MIME_TYPE)
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
    response["Content-Length"] = len(buffer.getvalue())
    return response


@require_GET
def descargar_contrato_ejemplo(request):
    """Descarga general de contrato (alias por defecto al deudor directo o por parámetro)."""
    if request.GET.get("tipo") == "fiador" or request.GET.get("fiador"):
        return descargar_contrato_fiador_ejemplo(request)
    return descargar_contrato_directo_ejemplo(request)


@require_GET
def descargar_contrato_directo_credito(request, credit_id):
    """
    Genera y descarga el Contrato de Reconocimiento de Deuda para Deudor Directo (.docx)
    vinculado a una Solicitud (InvestmentPlan) o Crédito real en el sistema.
    """
    credito = _resolver_objeto_credito_o_404(credit_id)

    overrides = {}
    if request.GET.get("deudor"):
        overrides["deudor_nombre"] = request.GET.get("deudor")
    if request.GET.get("monto"):
        try:
            overrides["monto_capital"] = float(request.GET.get("monto"))
        except ValueError:
            pass
    if request.GET.get("acta"):
        overrides["acta_numero"] = request.GET.get("acta")
    if request.GET.get("resolucion"):
        overrides["resolucion_ente"] = request.GET.get("resolucion")

    datos = extraer_datos_contrato_deudor_directo_desde_solicitud(credito, overrides=overrides or None)
    buffer = generar_contrato_deudor_directo_word(datos)

    codigo_raw = getattr(credito, "investment_plan_code", None) or getattr(credito, "codigo_credito", None) or f"id_{credito.id}"
    codigo_seguro = str(codigo_raw).replace("/", "-").replace(" ", "_")
    nombre_archivo = f"contrato_reconocimiento_deudor_directo_{codigo_seguro}.docx"

    response = HttpResponse(buffer.getvalue(), content_type=DOCX_MIME_TYPE)
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
    response["Content-Length"] = len(buffer.getvalue())
    return response


@require_GET
def descargar_contrato_fiador_credito(request, credit_id):
    """
    Genera y descarga el Contrato de Reconocimiento de Deuda Con Fiador(es) Solidario(s) (.docx)
    vinculado a una Solicitud (InvestmentPlan) o Crédito real en el sistema.
    Soporta dinámicamente todos los fiadores registrados en la solicitud (1, 2, 3, 5 o N fiadores).
    """
    credito = _resolver_objeto_credito_o_404(credit_id)

    overrides = {}
    if request.GET.get("deudor"):
        overrides["deudor_nombre"] = request.GET.get("deudor")
    if request.GET.get("monto"):
        try:
            overrides["monto_capital"] = float(request.GET.get("monto"))
        except ValueError:
            pass
    if request.GET.get("acta"):
        overrides["acta_numero"] = request.GET.get("acta")
    if request.GET.get("resolucion"):
        overrides["resolucion_ente"] = request.GET.get("resolucion")

    datos = extraer_datos_contrato_con_fiador_desde_solicitud(credito, overrides=overrides or None)
    if request.GET.get("fiador") and len(datos.get("fiadores", [])) > 0:
        datos["fiadores"][0]["nombre"] = request.GET.get("fiador")
        datos["fiador_nombre"] = request.GET.get("fiador")

    buffer = generar_contrato_con_fiador_word(datos)

    codigo_raw = getattr(credito, "investment_plan_code", None) or getattr(credito, "codigo_credito", None) or f"id_{credito.id}"
    codigo_seguro = str(codigo_raw).replace("/", "-").replace(" ", "_")
    cant_fiadores = len(datos.get("fiadores", []))
    sufijo = f"con_{cant_fiadores}_fiadores" if cant_fiadores > 1 else "con_fiador"
    nombre_archivo = f"contrato_reconocimiento_{sufijo}_{codigo_seguro}.docx"

    response = HttpResponse(buffer.getvalue(), content_type=DOCX_MIME_TYPE)
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
    response["Content-Length"] = len(buffer.getvalue())
    return response


descargar_contrato_directo_solicitud = descargar_contrato_directo_credito
descargar_contrato_fiador_solicitud = descargar_contrato_fiador_credito


def panel_descarga_pagare(request):
    """
    Página web interactiva con botones y enlaces directos para descargar
    todos los documentos Word legales generados.
    """
    credit_id_query = request.GET.get("credit_id")
    if credit_id_query:
        try:
            return descargar_pagare_credito(request, int(credit_id_query))
        except (ValueError, Http404):
            pass

    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>El Telar - Descargar Documentos Legales en Word</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            .card { border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border: none; }
            .header-banner { background: linear-gradient(135deg, #1b3a4b 0%, #006466 100%); color: white; border-radius: 12px 12px 0 0; padding: 25px; }
            .btn-download-primary { background-color: #2b7a78; border-color: #2b7a78; color: white; font-weight: 600; padding: 12px 20px; border-radius: 8px; text-decoration: none; }
            .btn-download-primary:hover { background-color: #17252a; border-color: #17252a; color: white; }
            .btn-download-secondary { background-color: #3a506b; border-color: #3a506b; color: white; font-weight: 600; padding: 12px 20px; border-radius: 8px; text-decoration: none; }
            .btn-download-secondary:hover { background-color: #1c2541; border-color: #1c2541; color: white; }
            .doc-card { border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px; margin-bottom: 16px; background-color: #ffffff; transition: transform 0.15s ease-in-out; }
            .doc-card:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.06); }
            .badge-tag { font-size: 0.75rem; padding: 5px 10px; border-radius: 4px; font-weight: 600; }
        </style>
    </head>
    <body class="py-5">
        <div class="container" style="max-width: 850px;">
            <div class="card">
                <div class="header-banner text-center">
                    <h3 class="mb-1">INVERSIONES INTEGRALES EL TELAR, S.A.</h3>
                    <p class="mb-0 text-white-50">Generador y Descargador de Plantillas Legales en Word (.docx)</p>
                </div>
                <div class="card-body p-4">
                    <p class="text-center text-muted mb-4">Selecciona el documento formal que deseas descargar en formato editable de Microsoft Word con todas las cláusulas notariales, montos en letras y firmas requeridas.</p>

                    <!-- DOCUMENTO 1: PAGARÉ LIBRE DE PROTESTO -->
                    <div class="doc-card">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <div>
                                <span class="badge bg-primary badge-tag">TÍTULO DE CRÉDITO</span>
                                <h5 class="mt-1 mb-1 font-weight-bold text-dark">1. Pagaré Libre de Protesto</h5>
                                <div class="text-muted small">Deudor: <strong>Mario Antonio Chen Caal</strong> | Monto: <strong>Q.360,000.00</strong> | Plazo: <strong>12 meses</strong> | Con Aval y Acta Notarial</div>
                            </div>
                            <a href="/documentos/pagare/ejemplo/" class="btn btn-download-primary btn-sm">
                                📥 Descargar (.docx)
                            </a>
                        </div>
                    </div>

                    <!-- DOCUMENTO 2: CONTRATO DEUDOR DIRECTO -->
                    <div class="doc-card">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <div>
                                <span class="badge bg-success badge-tag">CONTRATO DIRECTO (2 PARTES)</span>
                                <h5 class="mt-1 mb-1 font-weight-bold text-dark">2. Contrato de Reconocimiento de Deuda (Sin Fiador)</h5>
                                <div class="text-muted small">Deudora: <strong>Candy Claramaría Cantoral Caal de Papa</strong> | Monto: <strong>Q.39,634.00</strong> | 12 cuotas | Garantía Mobiliaria / Sueldo</div>
                            </div>
                            <a href="/documentos/contrato/directo/ejemplo/" class="btn btn-download-primary btn-sm">
                                📥 Descargar (.docx)
                            </a>
                        </div>
                    </div>

                    <!-- DOCUMENTO 3: CONTRATO CON FIADOR(ES) SOLIDARIO(S) -->
                    <div class="doc-card">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <div>
                                <span class="badge bg-info text-dark badge-tag">CON FIADORES SOLIDARIOS (1 A N FIADORES)</span>
                                <h5 class="mt-1 mb-1 font-weight-bold text-dark">3. Contrato de Reconocimiento de Deuda (Dinámico con Fiadores)</h5>
                                <div class="text-muted small">Deudora: <strong>Estefany Yusela López Ruiz</strong> | Soporta 1, 2, 3, 5 o más fiadores con cláusulas individuales, garantías y legalización notarial completa.</div>
                            </div>
                        </div>
                        <div class="d-flex flex-wrap gap-2">
                            <a href="/documentos/contrato/fiador/ejemplo/?num_fiadores=1" class="btn btn-download-secondary btn-sm">
                                📥 1 Fiador (.docx)
                            </a>
                            <a href="/documentos/contrato/fiador/ejemplo/?num_fiadores=2" class="btn btn-outline-secondary btn-sm">
                                📥 2 Fiadores (.docx)
                            </a>
                            <a href="/documentos/contrato/fiador/ejemplo/?num_fiadores=3" class="btn btn-outline-secondary btn-sm">
                                📥 3 Fiadores (.docx)
                            </a>
                            <a href="/documentos/contrato/fiador/ejemplo/?num_fiadores=5" class="btn btn-outline-secondary btn-sm">
                                📥 5 Fiadores (.docx)
                            </a>
                        </div>
                    </div>

                    <hr class="my-4">

                    <!-- Descargar por Crédito del Sistema -->
                    <div class="mb-4">
                        <h6 class="text-uppercase text-secondary font-weight-bold small mb-2">Descargar Pagaré de un Crédito del Sistema</h6>
                        <form method="GET" action="/documentos/pagare/" class="row g-2">
                            <div class="col-8">
                                <input type="number" name="credit_id" class="form-control" placeholder="Ingresa el ID del Crédito (ej. 1, 2, ...)" required>
                            </div>
                            <div class="col-4">
                                <button type="submit" class="btn btn-outline-primary w-100 font-weight-bold">Descargar Pagaré</button>
                            </div>
                        </form>
                    </div>

                    <!-- Enlaces Directos -->
                    <div class="bg-light p-3 rounded">
                        <h6 class="font-weight-bold text-dark small mb-2">Enlaces Directos de Descarga:</h6>
                        <ul class="list-unstyled small mb-0">
                            <li class="mb-1">🔹 <strong>Pagaré:</strong> <code><a href="/documentos/pagare/ejemplo/">/documentos/pagare/ejemplo/</a></code></li>
                            <li class="mb-1">🔹 <strong>Contrato Directo (Candy):</strong> <code><a href="/documentos/contrato/directo/ejemplo/">/documentos/contrato/directo/ejemplo/</a></code></li>
                            <li class="mb-1">🔹 <strong>Contrato con Fiador (Estefany & Fredy):</strong> <code><a href="/documentos/contrato/fiador/ejemplo/">/documentos/contrato/fiador/ejemplo/</a></code></li>
                            <li class="mb-1">🔹 <strong>Pagaré por ID (Solicitud/Crédito):</strong> <code>/documentos/pagare/&lt;credit_id&gt;/</code></li>
                            <li class="mb-1">🔹 <strong>Contrato Directo por ID (Solicitud/Crédito):</strong> <code>/documentos/contrato/directo/&lt;credit_id&gt;/</code></li>
                            <li>🔹 <strong>Contrato con Fiador(es) por ID (Solicitud/Crédito):</strong> <code>/documentos/contrato/fiador/&lt;credit_id&gt;/</code></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)
