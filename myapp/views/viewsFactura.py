from django.shortcuts import render
from django.http.response import JsonResponse
from ..models import Mesa
from ..models import Pedido
from ..models import Factura
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import re

def datos_facturas(request):
    # Obtener todas las facturas
    facturas = Factura.objects.all()

    # Inicializar listas para fechas y valores
    fechas = [factura.fecha.strftime('%Y-%m-%d') for factura in facturas]
    valores = [float(factura.valor) for factura in facturas]
    
    # Diccionario para acumular las cantidades de productos vendidos por cada mesero
    cantidad_por_mesero = {}
    # Diccionario para acumular las cantidades de productos vendidos por cada mesa
    cantidad_por_mesa = {}

    # Recorrer cada factura y extraer las cantidades de los productos
    for factura in facturas:
        # Extraer la lista de productos y cantidades usando regex
        productos = re.findall(r'([A-Za-z\s]+)\s\(Cantidad:\s(\d+)\)', factura.cosasPedidas)

        # Iterar sobre los productos y acumular las cantidades
        for producto, cantidad in productos:
            cantidad = int(cantidad)

            # Acumulando las ventas por mesero
            mesero_id = factura.idMesero.id
            if mesero_id in cantidad_por_mesero:
                cantidad_por_mesero[mesero_id]['cantidad'] += cantidad
            else:
                cantidad_por_mesero[mesero_id] = {'nombre': factura.idMesero.username, 'cantidad': cantidad}

            # Acumulando las ventas por mesa
            mesa_id = factura.mesa.idMesa
            if mesa_id in cantidad_por_mesa:
                cantidad_por_mesa[mesa_id]['cantidad'] += cantidad
            else:
                cantidad_por_mesa[mesa_id] = {'nombre': f'Mesa {factura.mesa.idMesa}', 'cantidad': cantidad}

    # Preparar los datos para la respuesta JSON
    # Datos de meseros
    nombres_meseros = [info['nombre'] for info in cantidad_por_mesero.values()]
    cantidades_vendidas_meseros = [info['cantidad'] for info in cantidad_por_mesero.values()]

    # Datos de mesas
    nombres_mesas = [info['nombre'] for info in cantidad_por_mesa.values()]
    cantidades_vendidas_mesas = [info['cantidad'] for info in cantidad_por_mesa.values()]

    # Crear el diccionario de datos para la respuesta JSON
    data = {
        'fechas': fechas,
        'valores': valores,
        'nombres_meseros': nombres_meseros,  # Nombres de los meseros
        'cantidades_vendidas_meseros': cantidades_vendidas_meseros,  # Cantidad total vendida por cada mesero
        'nombres_mesas': nombres_mesas,  # Nombres de las mesas
        'cantidades_vendidas_mesas': cantidades_vendidas_mesas  # Cantidad total vendida por cada mesa
    }

    return JsonResponse(data)



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

