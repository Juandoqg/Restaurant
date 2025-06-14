from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/verMesas/$', consumers.MeseroConsumer.as_asgi()),
    re_path(r'^ws/chef/$', consumers.ChefConsumer.as_asgi()),
    re_path(r'^ws/administrador/$', consumers.AdminChartConsumer.as_asgi()),


]
