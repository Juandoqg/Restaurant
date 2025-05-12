from django.http import HttpResponseNotAllowed, HttpResponseServerError, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from django.contrib.auth import login, logout, authenticate
from ..models import User
from ..models import Mesa
from ..models import Producto
from ..models import Pedido
from ..models import Factura
from mysite import settings
from django.contrib.auth.decorators import login_required
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.dateformat import DateFormat
# Create your views here.

@login_required
def verMesas(request):
    user_id = request.user.id
    users = User.objects.get(id=user_id)
    return render(request,'verMesas.html',{'users':users})

@login_required 
def listMesas(request):
    mesa = list(Mesa.objects.filter(visible=True).values())
    data = {'mesa': mesa}
    return JsonResponse(data)


def listMesasPorId(request, idMesa):
    if request.method == 'GET':
        mesa = get_object_or_404(Mesa, idMesa=idMesa)
        data = {
            'idMesa': mesa.idMesa,
            'numero': mesa.numero,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    

@login_required
def crearMesas(request):
    if request.method == 'GET':
        return render(request, 'crearMesas.html')
    elif request.method == 'POST':
        try:
            num_tables = int(request.POST['num_tables'])
            tipo = request.POST['tipo']
            descripcion = request.POST['descripcion']
            disponible = 'disponible' in request.POST

            # Crear las mesas
            for i in range(num_tables):
                mesa = Mesa.objects.create(
                    tipo=tipo,
                    descripcion=descripcion,
                    disponible=disponible
                )
                mesa.numero = mesa.idMesa  # Asignar el campo 'numero' igual al valor de 'id'
                mesa.save()

            return render(request, 'crearMesas.html', {'success': True})
        except Exception as e:
            return render(request, 'crearMesas.html', {'success': False, 'error': str(e)})


  # MESAS DEL ADMINISTRADOR
        
@login_required
def Mesas(request):
    mesas = Mesa.objects.filter(visible=True)
    return render(request,'Mesas.html',{'mesas':mesas})

@login_required
def borrar_mesa(request, producto_id):
    mesa = get_object_or_404(Mesa, pk=producto_id)
    mesa.visible = False
    mesa.save()
    return redirect('mesas')


@login_required
def editar_mesa(request, producto_id):
    mesa = get_object_or_404(Mesa, pk=producto_id)

    if request.method == 'POST':
        mesa.tipo = request.POST.get('tipo')
        mesa.descripcion = request.POST.get('descripcion')
        mesa.disponible = 'disponible' in request.POST
        mesa.save()
        return redirect('mesas')

    return render(request, 'editar_mesa.html', {'mesa': mesa})

