from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from ..models import User
from ..models import Pedido
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from ..factories.user_factory import UsuarioFactory

def signin(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    elif request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            if user is None:
                errors = {}
                if not username:
                    errors = "Por favor, introduce tu nombre de usuario."
                if not password:
                    errors = "Por favor, introduce tu contraseña."
                else:
                    errors = "El nombre de usuario o la contraseña no coinciden."
                return render(request, 'index.html', {'error': True, 'error_message': errors})
            else :
             login(request, user)
             success_url = ''
             if user.is_waiter:
                success_url = '/verMesas'
             elif user.is_chef:
                success_url = '/chef'
             elif user.is_superuser:
                success_url = '/administrador'
            
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

    