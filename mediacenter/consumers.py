from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels_presence.models import Room
from channels_presence.decorators import remove_presence
from mediacenter.models import RoomSetting
import json
from urllib.parse import parse_qs
from django.db.models.aggregates import Count
from random import randint


class PlayerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = parse_qs(self.scope['query_string'].decode('utf-8'))
        room = query_string.get('room', None)
        
        if not room:
            client_url = self.scope['client'][0]

            client_ip = client_url.split('.')[-1]
            self.room_name = client_ip
            self.room_group_name = 'player_%s' % self.room_name

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        else:
            room = room[0]
            client_ip = room.split('_')[-1]
            self.room_name = client_ip
            self.room_group_name = room

        await self.accept()

        await database_sync_to_async(self.add_room)()

        message = 'Player socket started.'

        source, source_type = await database_sync_to_async(self.get_source)()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join_or_leave_room',
                'message': message,
                'state': 'join',
            }
        )

        if not room:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_source',
                    'message': source,
                    'state': 'source',
                    'player_type': source_type
                }
            )

    def add_room(self):
        self.room = Room.objects.add(
            self.room_group_name, 
            self.channel_name,
            self.scope['user']
        )

        self.settings, created = RoomSetting.objects.get_or_create(
            room=self.room
        )

    def get_source(self):
        self.settings.refresh_from_db()
        if self.settings.player_type == RoomSetting.VIDEO:
            count = self.settings.videos.aggregate(count=Count('id'))['count']
            if count:
                random_index = randint(0, count - 1)
                video = self.settings.videos.all()[random_index]
                return (video.get_file_path(), 'video')
        else:
            count = self.settings.photos.aggregate(count=Count('id'))['count']
            if count:
                random_index = randint(0, count - 1)
                photo = self.settings.photos.all()[random_index]
                return (photo.get_file_path(), 'photo')

        return ('', None)

    async def disconnect(self, close_code):

        message = 'Player Socket ended'

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join_or_leave_room',
                'message': message,
                'state': 'leave',
            }
        )

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await database_sync_to_async(self.remove_room)()

    def remove_room(self):
        Room.objects.remove(
            self.room_group_name, 
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action', None)

        if action not in ['refresh']:
            message = {
                'type': 'button_action',
                'action': action
            }
        else:
            source, source_type = await database_sync_to_async(self.get_source)()

            message = {
                'type': 'send_source',
                'message': source,
                'state': 'source',
                'player_type': source_type
            }
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            message
        )

    # Receive message from room group
    async def button_action(self, event):
        action = event['action']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': {
                'action': action,
                'type': 'action',
            },
        }))

    async def join_or_leave_room(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': {
                'text': message,
                'type': event['state'],
            },
        }))

    async def send_source(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': {
                'source': message,
                'type': event['state'],
                'player_type': event['player_type']
            },
        }))
