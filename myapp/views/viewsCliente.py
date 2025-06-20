from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from ..models import Mesa
from ..factories.user_factory import UsuarioFactory
from django.shortcuts import render, redirect
from ..models import Reserva  # Importa tu modelo personalizado
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import re

def es_contrasena_valida(password):
    """Valida que la contraseña tenga al menos 8 caracteres, una mayúscula, un número y un carácter especial."""
    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"\d", password) or
        not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password)):
        return False
    return True

@csrf_exempt
def createClient(request):
    if request.method == 'POST':
        password = request.POST.get("password")
        # validación personalizada
        if not es_contrasena_valida(password):
            return render(request, 'registroCliente.html', {
                'messages': ['La contraseña debe tener al menos 8 caracteres, una mayúscula, un número y un carácter especial.'],
                'data': request.POST
            })

        user = UsuarioFactory.crear_usuarioCliente(request.POST)
        user.save()
        return render(request, 'registroCliente.html', {
            'messages': ['¡Cliente registrado exitosamente!']
        })

    return render(request, 'registroCliente.html')



def reservaCliente(request):
    if request.method == 'GET':
        return render(request, 'reservaCliente.html')
    
def reservarMesas(request):
    mesas = Mesa.objects.filter(disponible = True, visible =True )
    if request.method =="GET":
        return render (request, 'reservaMesasCliente.html', {'mesas': mesas})

@login_required
def verReservasCliente(request):
    reservas = Reserva.objects.filter(cliente=request.user).select_related('mesa').order_by('-fecha', '-hora')
    return render(request, 'verReservasCliente.html', {'reservas': reservas})
    

def reservarMesa(request, idMesa):
    mesa = get_object_or_404(Mesa, idMesa=idMesa, disponible=True, visible=True)

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        if not fecha or not hora:
            return render(request, 'reservarMesaCliente.html', {
                'mesa': mesa,
                'today': date.today().isoformat(),
                'error': True,
                'error_message': 'Debes seleccionar fecha y hora para reservar.'
            })

        # Guardar reserva
        Reserva.objects.create(
            mesa=mesa,
            cliente=request.user,
            fecha=fecha,
            hora=hora
        )
        mesa.disponible = False
        mesa.save()

        # Redirigir a una página separada con SweetAlert
        return redirect('reservaExitosa')

    return render(request, 'reservarMesaCliente.html', {
        'mesa': mesa,
        'today': date.today().isoformat()
    })

def lista_mesas_para_reservar(request):
    mesas = Mesa.objects.filter(disponible=True, visible=True).order_by('numero')
    return render(request, 'verMesasCliente.html', {'mesas': mesas})

def reservaExitosa(request):
    return render(request, 'reservaExitosa.html')
