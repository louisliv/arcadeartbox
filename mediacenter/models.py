from django.db import models
from channels_presence.models import Room

# Create your models here.

class Photo(models.Model):
    file_path = models.FileField(upload_to='photos/')

    def get_file_path(self):
        if self.file_path:
            return self.file_path.url

        return None

    def __str__(self):
        local_path = self.file_path.name 
        return local_path.split('/')[-1]

class Video(models.Model):
    file_path = models.FileField(upload_to='video/')

    def get_file_path(self):
        if self.file_path:
            return self.file_path.url

        return None

    def __str__(self):
        local_path = self.file_path.name 
        return local_path.split('/')[-1]

class RoomSetting(models.Model):
    VIDEO = 'Video'
    PHOTO = 'Photo'
    PLAYER_TYPES= [
        (VIDEO, 'Video'),
        (PHOTO, 'Photo')
    ]
    room = models.OneToOneField(Room, 
        on_delete=models.CASCADE, related_name="settings")
    room_name = models.CharField(
        max_length=144,
        blank=True
    )
    player_type = models.CharField(
        max_length=5,
        choices=PLAYER_TYPES,
        default=VIDEO,
    )
    videos = models.ManyToManyField(
        Video, 
        related_name='videos',
        blank=True
    )
    photos = models.ManyToManyField(
        Photo,
        related_name='photos',
        blank=True
    )

    def __str__(self):
        if not self.room_name:
            return self.room.channel_name

        return self.room_name