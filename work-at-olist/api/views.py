from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import Node


def handle_query(request):
    if request.GET == {}:
        return render(request, 'api/index.html')
    elif 'channels' in request.GET:
        return channels(request)
    elif 'channel' in request.GET and 'category' in request.GET:
        category_name = request.GET.get('category')
        channel_name = request.GET.get('channel')
        return category(request, channel_name, category_name)
    elif 'channel' in request.GET:
        channel_name = request.GET.get('channel')
        return channel(request, channel_name)
    elif 'preety' in request.GET:
        redirect('/')
    else:
        raise Http404


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
                'tree': category_node.tree.split('\n'),
                'branch': category_node.branch}
        if 'preety' in request.GET:
            context = json
            context['title'] = 'category: '+category_name
            return render(request, 'api/category.html', context)
        else:
            return JsonResponse(json)
