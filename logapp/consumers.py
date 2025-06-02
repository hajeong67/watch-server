from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("✅ WebSocket 연결됨")

    async def disconnect(self, close_code):
        print("❌ WebSocket 끊김")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print("수신 데이터:", data)
        await self.send(text_data=json.dumps({"status": "received"}))
