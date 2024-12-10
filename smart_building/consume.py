# your_app_name/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class IoTConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "iot_updates"
        self.room_group_name = "iot_group"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'iot_message',
                'message': data,
            }
        )

    async def iot_message(self, event):
        await self.send(text_data=json.dumps(event["message"]))
