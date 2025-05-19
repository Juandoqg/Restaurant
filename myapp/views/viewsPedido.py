from django.shortcuts import render, redirect
from ..models import Producto
from ..models import Pedido
from ..models import Mesa
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
import json
from django.utils import timezone
from ..decorators import admin_required, waiter_required, chef_required

@waiter_required
def enviar_factura(request, idMesa):
    # Obtén los datos necesarios de la factura (por ejemplo, pedidos, total, etc.)
    pedidos = Pedido.objects.filter(mesa=idMesa)  # Filtra los pedidos por la mesa
    mesa = Mesa.objects.get(idMesa=idMesa)
    total = sum([pedido.idProducto.precio * pedido.cantidad for pedido in pedidos])
    total_quantity = sum([pedido.cantidad for pedido in pedidos])

    user_id = pedidos.first().idMesero.id
    hora_actual = timezone.now()

    data = json.loads(request.body)
    destinatario = data.get('email')
    # Renderiza la plantilla HTML como string
    html_content = render_to_string('factura_email.html', {
                'idMesa': mesa.numero,
                'user_id': user_id,  # Aquí accedemos al id del mesero del primer pedido
                'pedidos': pedidos,
                'hora': hora_actual,
                'total': total,
                'total_quantity': total_quantity,
            })
    if not destinatario:
        return JsonResponse({'error': 'Por favor, proporciona un correo electrónico.'}, status=400)

    # Crea el correo
    email = EmailMessage(
        subject='Factura de La Patrana',
        body=html_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[destinatario],
    )
    email.content_subtype = 'html'  # Define que el contenido es HTML
    email.send()
    Pedido.objects.filter(mesa=idMesa).delete()

    # Redirigir a la vista de mesas después de enviar el correo y eliminar los pedidos
    return JsonResponse({'message': 'Correo enviado correctamente.'})
    


@waiter_required
def verPedido(request, idMesa):
    pedidos = Pedido.objects.filter(mesa__numero=idMesa)
    return render(request, 'verPedido.html', {'pedidos': pedidos, 'idMesa': idMesa})

@waiter_required
def tomarPedido(request, idMesa):
    # Obtener solo los productos disponibles
    productos_disponibles = Producto.objects.filter(disponible=True, visible =True)
    idMesa = idMesa
    return render(request, 'tomarPedido.html', {'Productos': productos_disponibles, 'idMesa': idMesa})


@waiter_required
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


@waiter_required
def borrarPedido (request, idMesa):
    Pedido.objects.filter(mesa=idMesa).delete()
    return redirect('verMesas')  

@login_required
def cambiar_estado_pedido(request, pedido_id):
    pedido = Pedido.objects.get(idPedido=pedido_id)
    pedido.hecho = not pedido.hecho  
    pedido.save()
    return redirect('chef') 