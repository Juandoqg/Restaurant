from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from ..factories.user_factory import UsuarioFactory
from django.shortcuts import render, redirect
from ..models import User  # Importa tu modelo personalizado
from django.contrib import messages

def createClient(request):
    if request.method == 'POST':
        user = UsuarioFactory.crear_usuarioCliente(request.POST)
        user.save()
        return render(request, 'registroCliente.html', {
            'messages': ['¡Cliente registrado exitosamente!']
        })

    return render(request, 'registroCliente.html')


def reservaCliente(request):
    if request.method == 'GET':
        return render(request, 'reservaCliente.html')