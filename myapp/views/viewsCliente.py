from django.shortcuts import render
from django.contrib.auth.decorators import login_required



from django.shortcuts import render, redirect
from ..models import User  # Importa tu modelo personalizado
from django.contrib import messages

def createClient(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        documento = request.POST.get('documento')
        documento = int(documento) if documento else None
        expedicion = request.POST.get('expedicion')
        fecha = request.POST.get('fecha')
        telefono = request.POST.get('telefono')
        contrasenia = request.POST.get('contrasenia')

        username = email.strip() if email else None

        user = User(
            username=username,
            first_name=nombre,
            last_name=apellido,
            email=email,
            documento=documento,
            expedicion=expedicion,
            fecha_nacimiento=fecha,
            telefono=telefono,
            is_client=True
        )
        user.set_password(contrasenia)
        user.save()

        # En vez de redirect, renderiza y pasa el mensaje en el contexto
        return render(request, 'registroCliente.html', {
            'messages': ['¡Cliente registrado exitosamente!']
        })

    return render(request, 'registroCliente.html')