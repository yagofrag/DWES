# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Tcomentarios(models.Model):
    comentario = models.CharField(max_length=2000)
    usuario = models.ForeignKey('Tusuarios', models.DO_NOTHING, blank=True, null=True)
    juego = models.ForeignKey('Tjuegos', models.DO_NOTHING)
    fecha_comentario = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tComentarios'


class tJuegos(models.Model):
    nombre = models.CharField(max_length=50)
    url_imagen = models.CharField(max_length=200, blank=True, null=True)
    genero = models.CharField(max_length=50, blank=True, null=True)
    plataforma = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tJuegos'


class Tusuarios(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=200)
    contraseña = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'tUsuarios'
