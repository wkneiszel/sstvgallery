from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Image, Comment
# Create your views here.

def index(request):
    return HttpResponse ("You've reached the site, hooray!")

def detail(request, image_id):
    return HttpResponse ("You've reached the detail page for image %s!" %image_id)


def gallery(request):
    latest_images_list = Image.objects.order_by('-receive_date')[:5]
    template = loader.get_template('sstvgallery/gallery.html')
    context = {
        'latest_images_list': latest_images_list,
    }
    return HttpResponse(template.render(context, request))