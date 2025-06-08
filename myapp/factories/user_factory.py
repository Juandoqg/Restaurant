# factories/user_factory.py

from myapp.models import User  # Asegúrate de importar desde tu app
from django.contrib.auth.hashers import make_password

class UsuarioFactory:
    @staticmethod
    def crear_usuario(datos):
        tipo = datos.get("Tipo")

        base_fields = {
            "username": datos["username"],
            "password": make_password(datos["password"]),  # encriptación
            "first_name": datos["name"],
            "last_name": datos["lastname"],
            "email": datos["email"],
            "documento": datos["document"],
            "expedicion": datos["date"],
            "telefono": datos["telefono"],
            "fecha_nacimiento" : datos["nacimiento"]
        }

        if tipo == "Mesero":
            base_fields["is_waiter"] = True
            base_fields["is_chef"] = False
        elif tipo == "Chef":
            base_fields["is_chef"] = True
            base_fields["is_waiter"] = False
        else:
            raise ValueError("Tipo de usuario no reconocido")

        return User(**base_fields)
