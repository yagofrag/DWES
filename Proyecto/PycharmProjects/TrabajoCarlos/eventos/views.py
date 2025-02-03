from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import json
from .models import usuarioPersonalizado, Evento, Reserva, Comentario


# ------------------- USUARIO -------------------
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        usuario = usuarioPersonalizado.objects.create_user(
            username=data['username'],
            password=data['password'],
            rol=data.get('rol', 'participante'),
            biografia=data.get('biografia', '')
        )
        return JsonResponse({'mensaje': 'Usuario registrado', 'id': usuario.id})


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        usuario = authenticate(username=data['username'], password=data['password'])
        if usuario:
            login(request, usuario)
            return JsonResponse({'mensaje': 'Login exitoso'})
        return JsonResponse({'error': 'Credenciales incorrectas'}, status=401)


# ------------------- EVENTOS -------------------
def listar_eventos(request):
    eventos = Evento.objects.select_related('organizador').all()

    # Filtros
    titulo = request.GET.get('titulo')
    fecha = request.GET.get('fecha')
    if titulo:
        eventos = eventos.filter(titulo__icontains=titulo)
    if fecha:
        eventos = eventos.filter(fecha_hora__date=fecha)

    # Paginación
    paginator = Paginator(eventos, 5)
    page = request.GET.get('page', 1)
    eventos_paginados = paginator.get_page(page)

    data = [
        {
            "id": e.id,
            "titulo": e.titulo,
            "descripcion": e.descripcion,
            "fecha_hora": e.fecha_hora.isoformat(),
            "capacidad_maxima": e.capacidad_maxima,
            "organizador": e.organizador.username
        }
        for e in eventos_paginados
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
def crear_evento(request):
    if request.method == 'POST':
        usuario = request.user
        if not usuario.is_authenticated or usuario.rol != 'organizador':
            return JsonResponse({'error': 'No autorizado'}, status=403)
        data = json.loads(request.body)
        evento = Evento.objects.create(
            titulo=data['titulo'],
            descripcion=data['descripcion'],
            fecha_hora=data['fecha_hora'],
            capacidad_maxima=data['capacidad_maxima'],
            imagen_url=data.get('imagen_url', ''),
            organizador=usuario
        )
        return JsonResponse({'mensaje': 'Evento creado', 'id': evento.id})


@csrf_exempt
def actualizar_evento(request, evento_id):
    if request.method in ['PUT', 'PATCH']:
        usuario = request.user
        evento = get_object_or_404(Evento, id=evento_id)
        if evento.organizador != usuario:
            return JsonResponse({'error': 'No autorizado'}, status=403)

        data = json.loads(request.body)
        evento.titulo = data.get('titulo', evento.titulo)
        evento.descripcion = data.get('descripcion', evento.descripcion)
        evento.fecha_hora = data.get('fecha_hora', evento.fecha_hora)
        evento.capacidad_maxima = data.get('capacidad_maxima', evento.capacidad_maxima)
        evento.imagen_url = data.get('imagen_url', evento.imagen_url)
        evento.save()

        return JsonResponse({'mensaje': 'Evento actualizado'})


@csrf_exempt
def eliminar_evento(request, evento_id):
    if request.method == 'DELETE':
        usuario = request.user
        evento = get_object_or_404(Evento, id=evento_id)
        if evento.organizador != usuario:
            return JsonResponse({'error': 'No autorizado'}, status=403)
        evento.delete()
        return JsonResponse({'mensaje': 'Evento eliminado'}, status=204)


# ------------------- RESERVAS -------------------
def listar_reservas(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)

    reservas = Reserva.objects.filter(usuario=request.user).select_related('evento').values(
        'id', 'evento__titulo', 'estado', 'numero_entradas'
    )

    return JsonResponse(list(reservas), safe=False)


@csrf_exempt
def crear_reserva(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'No autenticado'}, status=401)
        data = json.loads(request.body)
        evento = Evento.objects.get(id=data['evento_id'])
        reserva = Reserva.objects.create(
            usuario=request.user,
            evento=evento,
            numero_entradas=data['numero_entradas']
        )
        return JsonResponse({'mensaje': 'Reserva creada', 'id': reserva.id})


@csrf_exempt
def actualizar_reserva(request, reserva_id):
    if request.method in ['PUT', 'PATCH']:
        usuario = request.user
        reserva = get_object_or_404(Reserva, id=reserva_id)

        if usuario.rol != 'organizador' and reserva.usuario != usuario:
            return JsonResponse({'error': 'No autorizado'}, status=403)

        data = json.loads(request.body)
        if usuario.rol == 'organizador':
            reserva.estado = data.get('estado', reserva.estado)
        reserva.numero_entradas = data.get('numero_entradas', reserva.numero_entradas)
        reserva.save()

        return JsonResponse({'mensaje': 'Reserva actualizada'})


@csrf_exempt
def cancelar_reserva(request, reserva_id):
    if request.method == 'DELETE':
        usuario = request.user
        reserva = get_object_or_404(Reserva, id=reserva_id)

        if reserva.usuario != usuario:
            return JsonResponse({'error': 'No autorizado'}, status=403)

        reserva.delete()
        return JsonResponse({'mensaje': 'Reserva cancelada'}, status=204)


# ------------------- COMENTARIOS -------------------
def listar_comentarios(request, evento_id):
    comentarios = Comentario.objects.filter(evento_id=evento_id).select_related('usuario').values(
        'id', 'usuario__username', 'texto', 'fecha_creacion'
    )
    return JsonResponse(list(comentarios), safe=False)


@csrf_exempt
def crear_comentario(request, evento_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'No autenticado'}, status=401)
        data = json.loads(request.body)
        comentario = Comentario.objects.create(
            usuario=request.user,
            evento_id=evento_id,
            texto=data['texto']
        )
        return JsonResponse({'mensaje': 'Comentario añadido', 'id': comentario.id})
