from django.db import models
from django.contrib.auth.models import AbstractUser

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
    organizador = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, limit_choices_to={'rol': 'organizador'})

    def __str__(self):
        return self.titulo




class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, limit_choices_to={'rol': 'participante'})
    numero_entradas = models.PositiveIntegerField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.evento.titulo}"




class Comentario(models.Model):
    texto = models.TextField()
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} comenta en {self.evento.titulo}"
