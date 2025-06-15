# locustfile.py
from locust import HttpUser, task, between
import random
import string
from datetime import datetime
class RestauranteUser(HttpUser):
    wait_time = between(1, 5)  # espera entre tareas

    @task
    def ver_productos(self):
        self.client.get("/listProductos/")
    @task
    def ver_facturas(self):
        self.client.get("/listFacturas/")

    @task
    def crear_usuario_cliente(self):
    # generar sufijo aleatorio
        sufijo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        email = f"cliente_{sufijo}@example.com"

        self.client.post("/registroCliente/", data={
            "nombre": "Juan",
            "apellido": "Pérez",
            "email": email,
            "password": "123456",
            "documento": f"{random.randint(10000000, 99999999)}",
            "expedicion": "2020-01-01",
            "telefono": f"3{random.randint(100000000, 999999999)}",
            "fecha": "1990-01-01"
        })