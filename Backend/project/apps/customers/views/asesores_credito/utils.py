# Modelo 
from apps.actividades.models import DetalleInformeCobranza

def _total_registros(reporte):
    return DetalleInformeCobranza.objects.filter(reporte=reporte).count()

def _total_pendientes_cobranza(reporte):
    return DetalleInformeCobranza.objects.filter(
        reporte=reporte, 
        cobranza__estado_cobranza__icontains="Pendiente"
    ).count()

def _total_vencidos_cobranza(reporte):
    return DetalleInformeCobranza.objects.filter(
        reporte=reporte, 
        cobranza__estado_cobranza__icontains="INCUMPLIDO"
    ).count()

def _total_completados_cobranza(reporte):
    return DetalleInformeCobranza.objects.filter(
        reporte=reporte, 
        cobranza__estado_cobranza__icontains="Completado"
    ).count()

def porcentajes_cobranza(reporte):
        total = _total_registros(reporte)
        if total == 0:
            return {"pendientes": 0, "vencidos": 0, "completados": 0}

        pendientes = (_total_pendientes_cobranza(reporte) / total) * 100
        vencidos = (_total_vencidos_cobranza(reporte) / total) * 100
        completados = (_total_completados_cobranza(reporte) / total) * 100

        return {
            "pendientes": str(round(pendientes, 2)),
            "vencidos": round(vencidos, 2),
            "completados": round(completados, 2),
        }