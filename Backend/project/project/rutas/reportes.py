
# VISTAS DE LOS REPORTES EN EXCEL
from project.reports_excel import *
from project.views import list_reportes_modulos

# DECORADOR
from django.contrib.auth.decorators import login_required

# URLS
from django.urls import path, include


urlpatterns_reports = [
    path('reporte/banco/',login_required(report_banco),name='reporte_banco_excel'),
    path('reporte/boletas_base/',login_required(report_base_boletas),name='report_base_boletas'),
    path('reporte/boletas_filter/',login_required(ReporteBaseBoletasExcelView.as_view()),name='report_base_boletas_filter'),
    path('reporte/asesores/',login_required(ReporteAsesoresExcelView.as_view()),name='report_base_asesores'),
    path('reporte/clientes/',login_required(ReporteClientesExcelView.as_view()),name='report_clientes'),
    path('reporte/desembolso/<str:mes>/<str:anio>/',login_required(report_desmbolso),name='report_desmbolso'),
    path('reporte/pagos/creditos/<str:anio>/<str:mes>/', login_required(report_pagos_generales),name='report_pagos_generales'),
    path('reporte/pagos/acreedores/<str:anio>/<str:mes>/', login_required(report_pagos_generales_acreedores),name='report_pagos_generales_acreedores'),
    path('reporte/pagos/seguros/<str:anio>/<str:mes>/', login_required(report_pagos_generales_seguros),name='report_pagos_generales_seguros'),

    path('reporte/creditos/',login_required(ReporteCreditos.as_view()),name='report_creditos_excel'),
    path('reporte/pagos/creditos/<str:filtro_seleccionado>/<str:anio>/<str:mes>/<str:total>/',login_required(report_pagos),name='reporte_pagos_excel'),
    path('reporte/pagos/acreedores/<str:filtro_seleccionado>/<str:anio>/<str:mes>/<str:total>/',login_required(report_pagos_acreedores),name='report_pagos_acreedores_excel'),
    path('reporte/pagos/seguros/<str:filtro_seleccionado>/<str:anio>/<str:mes>/<str:total>/',login_required(report_pagos_seguros),name='report_pagos_seguros_excel'),
    path('reportes/clasificacion/', list_reportes_modulos,name='clasificacion_reportes'),
    path('reportes/ingresos/', login_required(ReporteIngresosExcelView.as_view()), name='report_ingresos'),
    path('reportes/egresos/', login_required(ReporteEgresosExcelView.as_view()), name='report_egresos'),

    path('reporte/cierre_diario/', login_required(CierreDiario.as_view()), name='reporte_cierre_datos'),
]