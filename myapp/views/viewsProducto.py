from django.shortcuts import render
from django.http.response import JsonResponse
from ..models import Producto
from mysite import settings
from django.contrib.auth.decorators import login_required
import os
from django.shortcuts import get_object_or_404, redirect

# Create your views here.

@login_required    
def listProductos(request):
   mesa = list(Producto.objects.values())
   data = {'producto': mesa}
   return JsonResponse(data) 

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
    Productos = Producto.objects.filter(visible=True)  # Solo los visibles
    return render(request, 'showProduct.html', {'Productos': Productos})

@login_required
def borrar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    producto.visible = False
    producto.save()
    return redirect('showProduct')

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    return render(request, 'showProduct.html', {'productos': producto})
