from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.nombre

class Experiencia(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    cupo_maximo = models.PositiveIntegerField()
    fecha_hora = models.DateTimeField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='experiencias')
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiencias_creadas')

    def cupos_disponibles(self):
        return self.cupo_maximo - self.inscripciones.count()

    def __str__(self):
        return self.titulo

class Inscripcion(models.Model):
    ESTADOS_PAGO = (
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
    )
    turista = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=15, choices=ESTADOS_PAGO, default='PENDIENTE')

    class Meta:
        unique_together = ('turista', 'experiencia')

    def __str__(self):
        return f"{self.turista.username} - {self.experiencia.titulo}"