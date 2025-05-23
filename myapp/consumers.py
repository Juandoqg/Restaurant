from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MeseroConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("meseros", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("meseros", self.channel_name)

    async def recibir_pedido(self, event):
        await self.send(text_data=json.dumps({
            "mensaje": event["mensaje"]
        }))


class ChefConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("chefs", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chefs", self.channel_name)

    async def nuevo_pedido(self, event):
        await self.send(text_data=json.dumps({
            "mensaje": event["mensaje"]
        }))
