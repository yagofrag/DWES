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