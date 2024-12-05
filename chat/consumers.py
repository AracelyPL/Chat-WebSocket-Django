import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "global_chat"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        
        messages = await self.load_messages()  # Cargar mensajes anteriores desde la base de datos
        for message in messages:
            await self.send(text_data=json.dumps({
                "user": message["user"],
                "message": message["content"],
            }))

    async def disconnect(self, close_code):
       
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
       
        text_data_json = json.loads(text_data)  # Procesar el mensaje recibido
        message = text_data_json["message"]
        user = text_data_json["user"]

        await self.save_message(user, message)  # Guardar el mensaje en la base de datos

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": user,
            }
        )

    async def chat_message(self, event):

        await self.send(text_data=json.dumps({  # Enviar el mensaje a WebSocket
            "user": event["user"],
            "message": event["message"],
        }))

    @sync_to_async
    def save_message(self, user, message):

        Message.objects.create(user=user, content=message) #Guarda un mensaje en la base de datos.

    @sync_to_async
    def load_messages(self):

        #Recupera los últimos 50 mensajes de la base de datos.
        messages = Message.objects.order_by('-timestamp')[:50]
        return reversed([{
            "user": message.user,
            "content": message.content
        } for message in messages])
