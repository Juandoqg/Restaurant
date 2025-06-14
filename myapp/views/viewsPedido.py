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
from ..decorators import admin_required, waiter_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



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
                    channel_layer = get_channel_layer()
                    mensaje = f"📥 Nuevo pedido en la mesa {idMesa}"
                    print("se esta enviadno")
                    async_to_sync(channel_layer.group_send)(
                        "chefs",  
                        {
                            "type": "nuevo_pedido",
                            "mensaje": mensaje
                        }
                    )

            return render(request, 'tomarPedido.html', {'success': True, 'idMesa': idMesa})
        
        except Exception as e:
            return render(request, 'tomarPedido.html', {'error': True, 'error_message': str(e), 'idMesa': idMesa})
    else:
        return render(request, 'tomarPedido.html', {'idMesa': idMesa})


@waiter_required
def borrarPedido (request, idMesa):
    Pedido.objects.filter(mesa=idMesa).delete()
    return redirect('verMesas')  

def cambiar_estado_pedido(request, pedido_id):
    pedido = Pedido.objects.get(idPedido=pedido_id)
    pedido.hecho = True  # o el nuevo estado que uses
    pedido.save()

    # Enviar mensaje a los meseros
    channel_layer = get_channel_layer()
    mensaje = f"🛎️ El pedido {pedido.idPedido} de la mesa {pedido.mesa.numero} está listo"

    async_to_sync(channel_layer.group_send)(
        "meseros",  # grupo al que están suscritos los meseros
        {
            "type": "recibir_pedido",
            "mensaje": mensaje
        }
    )

    return redirect('chef')