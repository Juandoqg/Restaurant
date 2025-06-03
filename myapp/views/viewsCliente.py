
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



def createClient(request):
    if request.method == 'GET':
            return render(request, 'registroCliente.html')  # Asegúrate de tener este template creado