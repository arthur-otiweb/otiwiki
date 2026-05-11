import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import MensagemChat

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            await self.channel_layer.group_add('chat_global', self.channel_name)
            await self.accept()
            await self.enviar_historico()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('chat_global', self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        mensagem = data['mensagem']
        
        await self.salvar_mensagem(mensagem)
        
        await self.channel_layer.group_send(
            'chat_global',
            {
                'type': 'chat_message',
                'usuario': self.user.username,
                'mensagem': mensagem,
                'timestamp': str(timezone.now())
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'usuario': event['usuario'],
            'mensagem': event['mensagem'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def salvar_mensagem(self, mensagem):
        MensagemChat.objects.create(usuario=self.user, mensagem=mensagem)

    @database_sync_to_async
    def enviar_historico(self):
        ultimas = MensagemChat.objects.all().order_by('-timestamp')[:50]
        return list(ultimas)