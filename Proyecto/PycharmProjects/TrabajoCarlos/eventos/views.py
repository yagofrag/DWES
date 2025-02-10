from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import json
from .models import usuarioPersonalizado, Evento, Reserva, Comentario
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

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
class ListarEventosAPIView(APIView):
    def get(self, request):
        eventos = Evento.objects.all()
        eventos_data = [
            {
                'id': evento.id,
                'titulo': evento.titulo,
                'descripcion': evento.descripcion,
                'fecha': evento.fecha_hora.isoformat(),
                'capacidad': evento.capacidad_maxima,
                'organizador': evento.organizador.username
            } for evento in eventos
        ]
        return JsonResponse(eventos_data, safe=False)


class CrearEventoAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.rol != 'organizador':
            return JsonResponse({'error': 'No tienes permisos para crear eventos'}, status=403)

        data = json.loads(request.body)
        evento = Evento.objects.create(
            organizador=request.user,
            titulo=data.get('titulo'),
            descripcion=data.get('descripcion'),
            fecha_hora=data.get('fecha_hora'),
            capacidad_maxima=data.get('capacidad_maxima'),
            imagen_url=data.get('imagen_url')
        )
        return JsonResponse({'mensaje': 'Evento creado correctamente', 'id': evento.id})

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


class CrearReservaAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = json.loads(request.body)
        evento_id = data.get('evento_id')
        numero_entradas = data.get('numero_entradas')

        try:
            evento = Evento.objects.get(id=evento_id)
        except Evento.DoesNotExist:
            return JsonResponse({'error': 'Evento no encontrado'}, status=404)

        reserva = Reserva.objects.create(
            usuario=request.user,
            evento_id=evento_id,
            numero_entradas=numero_entradas
        )
        return JsonResponse({'mensaje': 'Reserva creada correctamente', 'id': reserva.id})



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


class CancelarReservaAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, reserva_id):
        reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
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


#TOKENS

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = usuarioPersonalizado.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id, 'username': user.username})