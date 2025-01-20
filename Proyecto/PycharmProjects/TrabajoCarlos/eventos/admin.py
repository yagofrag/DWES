from django.contrib import admin
from .models import UsuarioPersonalizado, Evento, Reserva, Comentario

class UsuarioPersonalizadoAdmin(admin.ModelAdmin):
    list_display = ('username', 'rol', 'email')
    list_filter = ('rol',)
    search_fields = ('username', 'email')

class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_hora', 'capacidad_maxima', 'organizador')
    list_filter = ('fecha_hora',)
    search_fields = ('titulo',)

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'numero_entradas', 'estado')
    list_filter = ('estado', 'evento')

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'texto', 'fecha_creacion')
    search_fields = ('usuario__username', 'evento__titulo')

admin.site.register(UsuarioPersonalizado, UsuarioPersonalizadoAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Comentario, ComentarioAdmin)
