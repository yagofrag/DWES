from django.shortcuts import render
from django.http import HttpResponse , JsonResponse

from .models import tJuegos

# Create your views here.
def pagina_de_prueba(request):
	return HttpResponse("<h1>HOLA CARACOLA</h1>");

def devolver_juegos(request):
    lista = tJuegos.objects.all()
    respuesta_final = []
    for fila_sql in lista:
        diccionario = {
            'id': fila_sql.id,
            'nombre': fila_sql.nombre,
            'genero': fila_sql.genero
        }
        respuesta_final.append(diccionario)
    return JsonResponse(respuesta_final, safe=False)



def devolver_juego_por_id(request, id_solicitado):
    juego = tJuegos.objects.get(id=id_solicitado)
    comentarios = juego.tcomentarios_set.all()
    lista_comentarios = []
    for fila_comentario_sql in comentarios:
        diccionario = {}
        diccionario['id'] = fila_comentario_sql.id
        diccionario['comentario'] = fila_comentario_sql.comentario
        lista_comentarios.append(diccionario)
    resultado = {
        'id': juego.id,
        'nombre': juego.nombre,
        'genero': juego.genero,
        'comentarios': lista_comentarios
    }
    return JsonResponse(resultado, json_dumps_params={'ensure_ascii': False})
