from django.shortcuts import render
from ..models import User
from ..models import Pedido
from django.contrib.auth.decorators import login_required
from ..decorators import  chef_required


@chef_required
def chef(request):
    user_id = request.user.id
    usuario = User.objects.get(id=user_id)
    pedidos = Pedido.objects.all()  # Obtén todos los pedidos
    return render(request, 'chef.html', {'usuario': usuario, 'pedidos': pedidos})