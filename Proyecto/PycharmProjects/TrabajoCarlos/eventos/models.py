from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UsuarioPersonalizado(AbstractUser):
    ROL_CHOICES = [
        ('organizador', 'Organizador'),
        ('participante', 'Participante'),
    ]
    rol = models.CharField(max_length=15, choices=ROL_CHOICES, default='participante')
    biografia = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"

    class Evento(models.Model):
        titulo = models.CharField(max_length=100)
        descripcion = models.TextField()
        fecha_hora = models.DateTimeField()
        capacidad_maxima = models.PositiveIntegerField()
        imagen_url = models.URLField(blank=True, null=True)
        organizador = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE,
                                        limit_choices_to={'rol': 'organizador'})

        def __str__(self):
            return self.titulo