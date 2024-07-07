import json
from channels.generic.websocket import WebsocketConsumer
from user.models import CustomUser
from .models import Chat
from datetime import date
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'chatroom'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        userid = CustomUser.objects.get(username=username)
        today = str(date.today())
        newmessage = Chat.objects.create(user_id=userid, message_text=message, posting_date=today)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
            'type':'chat_message',
            'message':message,
            'date': today,
            }
        )

    def chat_message(self, event):
        message = event['message']
        today = event['date']
        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message,
            'date': today,
        }))


