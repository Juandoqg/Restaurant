from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    documento = models.IntegerField(null=True)
    expedicion = models.DateField(null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)  
    telefono = models.CharField(max_length=20, null=True, blank=True)  
    is_chef = models.BooleanField(default=False)
    is_waiter = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    visible = models.BooleanField(default=True) 

class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)
    disponible = models.BooleanField(default=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    nombre = models.CharField(max_length=50, default="")
    imgProducto = models.ImageField(upload_to='img/', null=True)
    visible = models.BooleanField(default=True) 


class Mesa(models.Model):
    idMesa = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=200, blank=True, null=True)
    numero = models.IntegerField(null=True, blank=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    visible = models.BooleanField(default=True)
    disponible = models.BooleanField(default=True)


class Pedido(models.Model):
    idPedido = models.AutoField(primary_key=True)
    numeroPedido = models.IntegerField()
    idMesero = models.ForeignKey(User, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    idProducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    hecho = models.BooleanField(default=False)
    nota = models.TextField(blank=True, null=True)

class Factura(models.Model):
    idFactura = models.AutoField(primary_key=True)
    valor = models.DecimalField(max_digits=20, decimal_places=2)
    hora = models.DateTimeField(null=True)
    fecha = models.DateField(null=True)
    cosasPedidas = models.CharField(max_length=400)
    idMesero = models.ForeignKey(User, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)

class Reserva(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name='reservas')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    fecha = models.DateField()
    hora = models.TimeField()
    creado_en = models.DateTimeField(auto_now_add=True)
