from django.shortcuts import render, redirect
from ..models import Producto
from ..models import Pedido
from django.contrib.auth.decorators import login_required
# Create your views here.

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
def borrarPedido (request, idMesa):
    Pedido.objects.filter(mesa=idMesa).delete()
    return redirect('verMesas')  

@login_required
def cambiar_estado_pedido(request, pedido_id):
    pedido = Pedido.objects.get(idPedido=pedido_id)
    pedido.hecho = not pedido.hecho  
    pedido.save()
    return redirect('chef') 