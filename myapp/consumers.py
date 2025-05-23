from channels.generic.websocket import AsyncWebsocketConsumer
import json

class PedidoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("meseros", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("meseros", self.channel_name)

    # Este método recibe mensajes del grupo y los reenvía al WebSocket
    async def recibir_pedido(self, event):
        await self.send(text_data=json.dumps({
            "mensaje": event["mensaje"]
        }))
