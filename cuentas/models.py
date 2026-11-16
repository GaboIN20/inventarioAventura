from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('GUIA', 'Guía / Operador'),
        ('TURISTA', 'Turista / Cliente'),
    )
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=10, choices=ROLES, default='TURISTA')
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.usuario.username} ({self.get_rol_display()})"