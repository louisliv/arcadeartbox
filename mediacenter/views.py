from django.shortcuts import render
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render
from django.db.models import Max
from mediacenter.globals import CONTROLLER_BUTTONS
from mediacenter.models import Video
from channels_presence.models import Room

import random

# Create your views here.

def player(request):
    context = {
        'is_video': False,
        'is_photo': False
    }
    max_id = Video.objects.all().aggregate(max_id=Max("id"))['max_id']

    if max_id:
        pk = random.randint(1, max_id)
        context['media_item'] = Video.objects.get(pk=pk)
        
    return render(request, 'mediacenter/player.html', context)

def controller(request, room):
    context = {
        'buttons': CONTROLLER_BUTTONS,
        'room': room
    }
        
    return render(request, 'mediacenter/controller.html', context)

class Players(ListView):
    model = Room
    template_name = 'mediacenter/player_list.html'