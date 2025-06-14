from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from ..models import Reserva
from ..models import Factura
from collections import defaultdict
import calendar, re
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from ..factories.user_factory import UsuarioFactory
from django.http.response import JsonResponse

def signin(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    elif request.method == 'POST':
        try:
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            errors = []

            if not username:
                errors.append("Por favor, introduce tu nombre de usuario.")
            if not password:
                errors.append("Por favor, introduce tu contraseña.")

            if errors:
                return render(request, 'index.html', {'error': True, 'error_message': " ".join(errors)})

            user = authenticate(request, username=username, password=password)
            if user is None:
                return render(request, 'index.html', {
                    'error': True,
                    'error_message': "Las credenciales son incorrectas."
                })
            else:
                login(request, user)

                success_url = ''
                if user.is_waiter:
                    success_url = '/verMesas'
                elif user.is_chef:
                    success_url = '/chef'
                elif user.is_superuser:
                    success_url = '/administrador'
                elif user.is_client:
                    success_url = '/reservaCliente'
                    
                return render(request, 'index.html', {'success': True, 'success_url': success_url})        
        except Exception as e:
            return render(request, 'index.html', {'error': True, 'error_message': str(e)})

@admin_required
def createUser(request):
    if request.method == 'GET':
        return render(request, 'createUser.html')
    else:
        try:
            user = UsuarioFactory.crear_usuario(request.POST)
            user.save()
            return render(request, 'createUser.html', {'success': True})
        except Exception as e:
            return render(request, 'createUser.html', {'success': False, 'error': str(e)})
        
@admin_required
def administrador(request):
    return render(request, 'administrador.html')

   
@login_required
def signout(request):
    logout(request)
    return redirect("/")    

@admin_required
def verReservas(request):
    reservas = Reserva.objects.select_related('mesa', 'cliente').all().order_by('-fecha', '-hora')
    return render(request, 'verReservas.html', {'reservas': reservas})


@admin_required
def consultas(request):
    return render(request, "consultas.html")


@admin_required
def datos_consultas(request):
    facturas = Factura.objects.all()
    reservas = Reserva.objects.all()

    # ----------------------------
    # Datos de facturas (ventas)
    # ----------------------------
    cantidad_por_mesero = {}
    cantidad_por_mesa = {}
    productos_vendidos = defaultdict(int)

    for factura in facturas:
        productos = re.findall(r'([A-Za-z\s]+)\s\(Cantidad:\s(\d+)\)', factura.cosasPedidas)

        for producto, cantidad in productos:
            cantidad = int(cantidad)

            # Mesero
            mesero_id = factura.idMesero.id
            if mesero_id in cantidad_por_mesero:
                cantidad_por_mesero[mesero_id]['cantidad'] += cantidad
            else:
                cantidad_por_mesero[mesero_id] = {'nombre': factura.idMesero.username, 'cantidad': cantidad}

            # Mesa
            mesa_id = factura.mesa.idMesa
            if mesa_id in cantidad_por_mesa:
                cantidad_por_mesa[mesa_id]['cantidad'] += cantidad
            else:
                cantidad_por_mesa[mesa_id] = {'nombre': f'Mesa {factura.mesa.idMesa}', 'cantidad': cantidad}

            # Producto
            productos_vendidos[producto.strip()] += cantidad

    # ----------------------------
    # Datos de reservas
    # ----------------------------
    reservas_por_mesero = defaultdict(int)
    reservas_por_mesa = defaultdict(int)
    reservas_por_fecha = defaultdict(int)

    for reserva in reservas:
        # Asumiendo que usuario es el mesero o quien reservó
        nombre_mesero = reserva.cliente.username if reserva.cliente else "Desconocido"
        reservas_por_mesero[nombre_mesero] += 1

        nombre_mesa = f"Mesa {reserva.mesa.idMesa}" if reserva.mesa else "Sin Mesa"
        reservas_por_mesa[nombre_mesa] += 1

        fecha = reserva.fecha.strftime('%Y-%m-%d')
        reservas_por_fecha[fecha] += 1

    # ----------------------------
    # Armar JSON de respuesta
    # ----------------------------
    data = {
        # Ventas
        'nombres_meseros': [info['nombre'] for info in cantidad_por_mesero.values()],
        'cantidades_vendidas_meseros': [info['cantidad'] for info in cantidad_por_mesero.values()],
        'nombres_mesas': [info['nombre'] for info in cantidad_por_mesa.values()],
        'cantidades_vendidas_mesas': [info['cantidad'] for info in cantidad_por_mesa.values()],
        'productos': list(productos_vendidos.keys()),
        'cantidades_productos': list(productos_vendidos.values()),

        # Reservas
        'reservas_meseros': list(reservas_por_mesero.keys()),
        'cantidad_reservas_meseros': list(reservas_por_mesero.values()),
        'reservas_mesas': list(reservas_por_mesa.keys()),
        'cantidad_reservas_mesas': list(reservas_por_mesa.values()),
        'fechas_reservas': list(reservas_por_fecha.keys()),
        'cantidad_reservas_fechas': list(reservas_por_fecha.values()),
    }

    return JsonResponse(data)
