from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Node


def channels(request):
    response = Node.objects.filter(parent=None)
    json = {"channels": []}
    for channel in response:
        json["channels"].append(channel.name)
    if 'preety' in request.GET:
        return render(request, 'api/channels.html',
                      {"channels": response, "title": "channels"})
    else:
        return JsonResponse(json)
