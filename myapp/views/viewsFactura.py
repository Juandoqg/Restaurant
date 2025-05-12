from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from ..models import Mesa
from ..models import Pedido
from ..models import Factura
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import re
import calendar

def datos_facturas(request):
    facturas = Factura.objects.all()

    fechas = [factura.fecha.strftime('%Y-%m-%d') for factura in facturas]
    valores = [float(factura.valor) for factura in facturas]

    cantidad_por_mesero = {}
    cantidad_por_mesa = {}
    productos_vendidos = defaultdict(int)
    ventas_por_dia = defaultdict(float)  # Nuevo: para acumular ventas por día de la semana

    for factura in facturas:
        productos = re.findall(r'([A-Za-z\s]+)\s\(Cantidad:\s(\d+)\)', factura.cosasPedidas)

        # Día de la semana (0=lunes, 6=domingo)
        dia_semana = factura.fecha.weekday()
        nombre_dia = calendar.day_name[dia_semana]
        ventas_por_dia[nombre_dia] += float(factura.valor)

        for producto, cantidad in productos:
            cantidad = int(cantidad)

            mesero_id = factura.idMesero.id
            if mesero_id in cantidad_por_mesero:
                cantidad_por_mesero[mesero_id]['cantidad'] += cantidad
            else:
                cantidad_por_mesero[mesero_id] = {'nombre': factura.idMesero.username, 'cantidad': cantidad}

            mesa_id = factura.mesa.idMesa
            if mesa_id in cantidad_por_mesa:
                cantidad_por_mesa[mesa_id]['cantidad'] += cantidad
            else:
                cantidad_por_mesa[mesa_id] = {'nombre': f'Mesa {factura.mesa.idMesa}', 'cantidad': cantidad}

            productos_vendidos[producto.strip()] += cantidad

    nombres_meseros = [info['nombre'] for info in cantidad_por_mesero.values()]
    cantidades_vendidas_meseros = [info['cantidad'] for info in cantidad_por_mesero.values()]

    nombres_mesas = [info['nombre'] for info in cantidad_por_mesa.values()]
    cantidades_vendidas_mesas = [info['cantidad'] for info in cantidad_por_mesa.values()]

    nombres_productos = list(productos_vendidos.keys())
    cantidades_productos = list(productos_vendidos.values())

    # Nuevo: convertir diccionario de ventas por día a listas
    dias_semana = list(ventas_por_dia.keys())
    ventas_dias = list(ventas_por_dia.values())

    data = {
        'fechas': fechas,
        'valores': valores,
        'nombres_meseros': nombres_meseros,
        'cantidades_vendidas_meseros': cantidades_vendidas_meseros,
        'nombres_mesas': nombres_mesas,
        'cantidades_vendidas_mesas': cantidades_vendidas_mesas,
        'productos': nombres_productos,
        'cantidades_productos': cantidades_productos,
        'dias_semana': dias_semana,
        'ventas_dias': ventas_dias
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
    facturas = Factura.objects.filter(visible=True)
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
def borrar_factura(request, factura_id):
    try:
        factura = Factura.objects.get(idFactura=factura_id)
        factura.visible = False  # Establecemos el estado visible a False
        factura.save()
    except Factura.DoesNotExist:
        # Aquí puedes manejar el error si la factura no existe
        pass
    return redirect('verFactura') 

