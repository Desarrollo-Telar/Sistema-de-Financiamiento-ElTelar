
# PATH
from django.urls import path, include

# VIEWS
from apps.actividades import views

urlpatterns_notificaciones = [
    path('notification/',views.listar_notificaciones, name='notification'),
    path('notification/<str:uuid>/',views.detalle_notificacion, name='detalle_notificacion'),
    path('notification/delete/<str:uuid>/',views.eliminar_notificacion, name='eliminar_notificacion'),
    path('cerrar_pestania/', views.cerrar_pestana, name='cerrar_pestania'),
    path('boletas_clientes/',views.DocumentoNotificacionClientesList.as_view(), name='listar_boletas_subidas'),
    path('boletas_clientes/<int:id>/',views.detalle_boleta_cliente, name='detalle_boleta_cliente'),
    path('boletas_clientes/aprobar/<int:id>/',views.aprobar_boleta_cliente, name='aprobar_boleta_cliente'),
    path('boletas_clientes/rechazar/<int:id>/',views.rechazar_boleta_cliente, name='rechazar_boleta_cliente'),
    
    
]