from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Node


def handle_query(request):
    if 'channels' in request.GET:
        return channels(request)
    elif 'channel' in request.GET and 'category' in request.GET:
        category_name = request.GET.get('category')
        channel_name = request.GET.get('channel')
        return category(request, channel_name, category_name)
    elif 'channel' in request.GET:
        channel_name = request.GET.get('channel')
        return channel(request, channel_name)


def channels(request):
    response = Node.objects.filter(parent=None)
    if 'preety' in request.GET:
        return render(request, 'api/channels.html',
                      {'channels': response, 'title': 'channels'})
    else:
        json = {'channels': []}
        for channel in response:
            json['channels'].append(channel.name)
        return JsonResponse(json)


def channel(request, channel_name):
    print(channel_name)
    channel_node = get_object_or_404(Node, name=channel_name, parent=None)
    json = {'channel': channel_name,
            'tree': channel_node.tree.split('\n')}
    if 'preety' in request.GET:
        context = json
        context['title'] = 'channel: '+channel_name
        return render(request, 'api/channel.html', context)
    else:
        return JsonResponse(json)


def category(request, channel_name, category_name):
    channel_node = get_object_or_404(Node, name=channel_name, parent=None)
    category_node = channel_node.find_category(category_name)
    if category_node is None:
        raise Http404
    else:
        json = {'channel': channel_name,
                'category': category_name,
                'tree': channel_node.tree.split('\n'),
                'branch': category_node}
        if 'preety' in request.GET:
            context = json
            context['title'] = 'category: '+category_name
            return render(request, 'api/category.html', context)
        else:
            return JsonResponse(json)
