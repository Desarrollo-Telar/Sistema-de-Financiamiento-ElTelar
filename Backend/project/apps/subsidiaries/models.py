from django.db import models


DIAS_SEMANA = [
    ('lunes', 'Lunes'),
    ('martes', 'Martes'),
    ('miercoles', 'Miércoles'),
    ('jueves', 'Jueves'),
    ('viernes', 'Viernes'),
    ('sabado', 'Sábado'),
    ('domingo', 'Domingo'),
]

# Create your models here.
class Subsidiary(models.Model):
    codigo_sucursal= models.CharField("Codigo de la Sucursal", max_length=100, blank=True, null=True)
    nombre = models.CharField("Nombre de la Sucursal", max_length=100, blank=True, null=True)
    fecha_apertura = models.DateField("Fecha de Apertura")
    numero_telefono = models.CharField("Numero de Telfono de la Sucursal", max_length=100, blank=True, null=True) 
    otro_numero_telefono = models.CharField("Otro Numero de Telfono de la Sucursal", max_length=100, blank=True, null=True) 
    activa = models.BooleanField("Status de la Actividad de la Sucursal", default=True)
    codigo_postal = models.CharField("Codigo Postal", blank=True, null=True, max_length=100)
    descripcion = models.TextField("Descripcion", blank=True, null=True)
    codigo_establecimiento = models.CharField("CODIGO DE ESTABLECIMIENTO", blank=True, null=True, default="1")

    def __str__(self):
        return f'{self.nombre}'

    @property
    def esta_abierta_ahora(self):
        import datetime
        hoy = datetime.datetime.today()
        dia = hoy.strftime('%A').lower()  # ejemplo: 'monday'
        horario = self.horarios.filter(dia=dia).first()
        if not horario or not horario.activo:
            return False
        return horario.hora_apertura <= hoy.time() <= horario.hora_cierre

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'

class HorarioSucursal(models.Model):
    sucursal = models.ForeignKey(Subsidiary, related_name='horarios', on_delete=models.CASCADE)
    dia = models.CharField(max_length=10, choices=DIAS_SEMANA)
    hora_apertura = models.TimeField("Hora de Apertura")
    hora_cierre = models.TimeField("Hora de Cierre")
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('sucursal', 'dia')
        verbose_name = 'Horario Sucursal'
        verbose_name_plural = 'Horarios Sucursales'

    def __str__(self):
        return f"{self.sucursal.nombre} - {self.dia.capitalize()}"