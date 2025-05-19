from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from ..models import User
from django.contrib.auth.decorators import login_required
import os
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateformat import DateFormat
from ..decorators import admin_required, waiter_required, chef_required


@admin_required   
def showUsers(request):
    users = User.objects.all()
    return render(request, 'showUsers.html', {'users': users})

@login_required
def listUsers(_request):
    user = list(User.objects.values())
    data = {'user': user}
    return JsonResponse(data)

def listUserPorId(request, user_id):
    if request.method == 'GET':
        usuario = get_object_or_404(User, id=user_id)
        
        # Crear un diccionario con los datos del usuario
        data = {
            'id': usuario.id,
            'email': usuario.email,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'username': usuario.username,
            'is_active': usuario.is_active,
            'is_waiter': usuario.is_waiter,
            'is_chef': usuario.is_chef,
            'is_superuser': usuario.is_superuser
        }
        
        return JsonResponse(data)  # Ahora `data` es un diccionario válido
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    

@admin_required    
def deleteUser(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    usuario.delete()
    return redirect('/showUsers')

@csrf_exempt
def actualizarDatosUsuario(request, user_id):
    if request.method == 'PUT':
        try:
            # Obtener el objeto User por su ID
            user = get_object_or_404(User, id=user_id)
            
            # Cargar los datos del cuerpo de la solicitud
            data = json.loads(request.body)

            # Actualizar los campos del usuario con los datos recibidos
            user.email = data.get('email', user.email)
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.username = data.get('username', user.username)
            
            # Determinar los valores de is_waiter y is_chef según el userType
            user_type = data.get('userType')
            if user_type == 'Mesero':
                user.is_waiter = True
                user.is_chef = False
            elif user_type == 'Chef':
                user.is_waiter = False
                user.is_chef = True
            else:
                # Si no es ni 'Mesero' ni 'Chef', asignar ambos como False
                user.is_waiter = False
                user.is_chef = False
            
            # Actualizar el estado de actividad (is_active) según el user_status
            user_status = data.get('user_status')
            if user_status == 'option1':  # Si está activo
                user.is_active = True
            else:  # Si no está activo
                user.is_active = False

            # Guardar los cambios en la base de datos
            user.save()
            
            # Devuelve una respuesta con los datos actualizados
            return JsonResponse({
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'is_active': user.is_active,
                'is_waiter': user.is_waiter,
                'is_chef': user.is_chef,
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        # Si el método no es PUT
        return HttpResponseNotAllowed(['PUT'])
    

def actualizarContra(request):
    if request.method == "GET":
        # Obtén los datos de la sesión
        documento = request.session.get('documento')
        expedicion = request.session.get('expedicion')
    

        return render(request, "actualizarContra.html", {
            'documento': documento,
            'expedicion': expedicion
        })
    elif request.method == "POST":
        try: 
         documento = request.session.get('documento')
         expedicion = request.session.get('expedicion')
         contra= request.POST.get("contra")
         confirmarContra = request.POST.get("confirmarContra")
         print("Contra:", contra)
         print("Contra:", confirmarContra)
         print(documento)
         print(expedicion)
         user = get_object_or_404(User, documento = documento , expedicion = expedicion)
         print(user.id)
         user.set_password(contra)
         user.save()
         return render(request, 'actualizarContra.html', {'success': True})
        except Exception as e:
            return render(request, 'actualizarContra.html', {'error': True, 'error_message': str(e)})
    return render(request, "actualizarContra.html")


def recuperarContra(request):
    if request.method == "GET":
        return render(request, "recuperarContra.html")
    elif request.method == "POST":
        try: 
         documento = request.POST["document"]
         expedicion = request.POST["date"]
         request.session["documento"] = documento
         request.session["expedicion"] = expedicion
         print(documento)
         print(expedicion)
         user = get_object_or_404(User, documento = documento , expedicion = expedicion)
         print(user.id)
         return render(request, 'recuperarContra.html', {'success': True})
        except Exception as e:
            return render(request, 'recuperarContra.html', {'error': True, 'error_message': str(e)})
    return render(request, "recuperarContra.html")