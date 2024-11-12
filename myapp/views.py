from django.http import HttpResponseNotAllowed, HttpResponseServerError, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from django.contrib.auth import login, logout, authenticate
from .models import User
from .models import Mesa
from .models import Producto
from .models import Pedido
from .models import Factura
from mysite import settings
from django.contrib.auth.decorators import login_required
import os
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from django.db.models import Sum
from django.utils.dateformat import DateFormat
# Create your views here.

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

@login_required
def createUser(request):
    if request.method == 'GET':
        return render(request, 'createUser.html')
    else:
        try:
            if request.POST["Tipo"] == 'Mesero':
                is_waiter = 1
                is_chef = 0
            else:
                is_chef = 1
                is_waiter = 0

            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password"],
                first_name=request.POST["name"],
                last_name=request.POST["lastname"],
                email=request.POST["email"],
                documento = request.POST["document"],
                expedicion = request.POST["date"],
                is_waiter=is_waiter,
                is_chef=is_chef
            )
            user.save()
            return render(request, 'createUser.html', {'success': True})
        except Exception as e:
            return render(request, 'createUser.html', {'success': False, 'error': str(e)}) 
        
@login_required
def administrador(request):
    return render(request, 'administrador.html')

def datos_facturas(request):

    # Obtener datos
    facturas = Factura.objects.all()

    fechas = [factura.fecha.strftime('%Y-%m-%d') for factura in facturas]
    valores = [float(factura.valor) for factura in facturas]


    data = {
        'fechas': fechas,
        'valores': valores
    }
    return JsonResponse(data)

@login_required
def verMesas(request):
    user_id = request.user.id
    users = User.objects.get(id=user_id)
    return render(request,'verMesas.html',{'users':users})
  
@login_required
def chef(request):
    user_id = request.user.id
    usuario = User.objects.get(id=user_id)
    pedidos = Pedido.objects.all()  # Obtén todos los pedidos
    return render(request, 'chef.html', {'usuario': usuario, 'pedidos': pedidos})

@login_required    
def showUsers(request):
    users = User.objects.all()
    return render(request, 'showUsers.html', {'users': users})

@login_required
def listUsers(_request):
    user = list(User.objects.values())
    data = {'user': user}
    return JsonResponse(data)

@login_required 
def listMesas(request):
   mesa = list(Mesa.objects.values())
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

@login_required    
def listProductos(request):
   mesa = list(Producto.objects.values())
   data = {'producto': mesa}
   return JsonResponse(data) 

@login_required    
def deleteUser(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    usuario.delete()
    return redirect('/showUsers')

@login_required
def createProduct(request):
    if request.method == 'GET':
        return render(request, 'createProduct.html')
    elif request.method == 'POST':
        try:
            # Convertir el valor del toggle a un booleano
            disponible = request.POST.get("toggleDisponible", False) == "on"

            # Obtener la instancia del Producto del formulario
            producto = Producto(
                nombre=request.POST["nombreProducto"],
                descripcion=request.POST["Descripcion"],
                precio=request.POST["Precio"],
                disponible=disponible
            )

            # Guardar la imagen en la carpeta restaurante/myapp/static/img
            if 'imgProducto' in request.FILES:
                imagen = request.FILES['imgProducto']
                ruta_imagen = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'img', imagen.name)
                with open(ruta_imagen, 'wb') as f:
                    for chunk in imagen.chunks():
                        f.write(chunk)
                producto.imgProducto = os.path.join('img/', imagen.name)

            # Guardar el producto en la base de datos
            producto.save()
            return render(request, 'createProduct.html', {'success': True})
        except Exception as e:
            return render(request, 'createProduct.html', {'success': False, 'error': str(e)})

@login_required            
def showProduct(request):
    Productos = Producto.objects.all()
    return render(request, 'showProduct.html', {'Productos': Productos})

@login_required
def verPedido(request, idMesa):
    pedidos = Pedido.objects.filter(mesa__numero=idMesa)
    return render(request, 'verPedido.html', {'pedidos': pedidos, 'idMesa': idMesa})

@login_required
def tomarPedido(request, idMesa):
    # Obtener solo los productos disponibles
    productos_disponibles = Producto.objects.filter(disponible=True)
    idMesa = idMesa
    return render(request, 'tomarPedido.html', {'Productos': productos_disponibles, 'idMesa': idMesa})


@login_required
def savePedido(request, idMesa):
    if request.method == 'POST':
        try:
            productos_seleccionados = request.POST.getlist('productos_seleccionados[]')
            cantidades = {key.split('_')[1]: value for key, value in request.POST.items() if key.startswith('cantidad_')}
            notas = {key.split('_')[1]: value for key, value in request.POST.items() if key.startswith('notas_')}
            
            idMesero = request.user.id
            
            for producto_id in productos_seleccionados:
                cantidad = int(cantidades.get(producto_id, 0))
                nota = notas.get(producto_id, '') 
                if cantidad > 0:
                    pedido = Pedido.objects.create(
                        numeroPedido=idMesa,
                        cantidad=cantidad,
                        nota=nota,
                        idMesero_id=idMesero,
                        mesa_id=idMesa,
                        idProducto_id=producto_id
                    )
                    pedido.save()
            return render(request, 'tomarPedido.html', {'success': True, 'idMesa': idMesa})
        
        except Exception as e:
            return render(request, 'tomarPedido.html', {'error': True, 'error_message': str(e), 'idMesa': idMesa})
    else:
        return render(request, 'tomarPedido.html', {'idMesa': idMesa})


@login_required
def cambiar_estado_pedido(request, pedido_id):
    pedido = Pedido.objects.get(idPedido=pedido_id)
    pedido.hecho = not pedido.hecho  
    pedido.save()
    return redirect('chef') 

@csrf_exempt
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

@login_required            
def verFacturaID(request, idMesa):
    pedidos = Pedido.objects.filter(mesa__numero=idMesa)
    
    if not pedidos.exists():
        # Redirigir o mostrar un mensaje si no hay pedidos
        return render(request, 'verMesas.html', {'idMesa': idMesa})
    
    user_id = request.user.id
    hora = timezone.localtime(timezone.now())
    fecha = hora.date()
    total = sum(pedido.idProducto.precio * pedido.cantidad for pedido in pedidos)
    total_quantity = sum(pedido.cantidad for pedido in pedidos)  # Calculate total quantity

    # Formatear los productos pedidos en un solo string
    cosas_pedidas = ', '.join([f"{pedido.idProducto.nombre} (Cantidad: {pedido.cantidad})" for pedido in pedidos])

    # Obtener la mesa
    mesa = Mesa.objects.get(numero=idMesa)

    # Crear y guardar la nueva factura
    factura = Factura(
        valor=total,
        hora=hora,
        fecha=fecha,
        cosasPedidas=cosas_pedidas,
        idMesero=request.user,
        mesa=mesa
    )
    factura.save()

    return render(request, 'verFacturaID.html', {
        'pedidos': pedidos,
        'user_id': user_id,
        'hora': hora,
        'idMesa': idMesa,
        'total': total,
        'total_quantity': total_quantity  
    })
@login_required
def verFactura(request):
    facturas = Factura.objects.all()
    processed_facturas = []

    for factura in facturas:
        productos = factura.cosasPedidas.split(', ')
        productos_procesados = []
        for producto in productos:
            nombre, cantidad = producto.rsplit(' (Cantidad: ', 1)
            cantidad = cantidad.rstrip(')')
            productos_procesados.append({
                'nombre': nombre,
                'cantidad': cantidad
            })
        processed_facturas.append({
            'factura': factura,
            'productos': productos_procesados
        })

    return render(request, 'verFactura.html', {'processed_facturas': processed_facturas})
@login_required
def borrarPedido (request, idMesa):
    Pedido.objects.filter(mesa=idMesa).delete()
    return redirect('verMesas')  

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



@login_required
def crearMesas(request):
    if request.method == 'GET':
        return render(request, 'crearMesas.html')
    elif request.method == 'POST':
        try:
            num_tables = int(request.POST['num_tables'])
            for i in range(num_tables):
             mesa = Mesa.objects.create()
             mesa.numero = mesa.idMesa  # Asignar el campo 'numero' igual al valor de 'id'
             mesa.save()


            # Guardar la imagen en la carpeta restaurante/myapp/static/img
            if 'imgProducto' in request.FILES:
                imagen = request.FILES['imgProducto']
                ruta_imagen = os.path.join(settings.BASE_DIR, 'myapp', 'static', 'img', imagen.name)
                with open(ruta_imagen, 'wb') as f:
                    for chunk in imagen.chunks():
                        f.write(chunk)
                Producto.imgProducto = os.path.join('img/', imagen.name)
            return render(request, 'crearMesas.html', {'success': True})
        except Exception as e:
            return render(request, 'crearMesas.html', {'success': False, 'error': str(e)})
   
@login_required
def signout(request):
    logout(request)
    return redirect("/")    

    