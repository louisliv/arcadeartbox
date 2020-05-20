from django.contrib.auth.models import User
from rest_framework import serializers
from mediacenter.models import RoomSetting
from channels_presence.models import Room


class RoomSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomSetting
        fields = ['id', 'room_name', 'player_type']


class RoomSerializer(serializers.ModelSerializer):
    settings = RoomSettingSerializer()
    channel_name = serializers.CharField()

    class Meta:
        model = Room
        fields = ['id', 'channel_name', 'settings']