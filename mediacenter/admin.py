from django.contrib import admin
from mediacenter.models import (Video, Photo,
    RoomSetting)
from channels_presence.models import Room

# Register your models here.
admin.site.register(Video)
admin.site.register(Photo)
admin.site.register(Room)
admin.site.register(RoomSetting)