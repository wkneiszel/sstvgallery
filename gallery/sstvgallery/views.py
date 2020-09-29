from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from rest_framework import viewsets
from .models import Image, Comment
from .serializers import ImageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import datetime
from rest_framework.exceptions import ParseError
import json
# Create your views here.

def index(request):
    return HttpResponse ("You've reached the site, hooray!")

def detail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    comments = image.comment_set.order_by('-comment_date')
    template = loader.get_template('sstvgallery/detail.html')
    context = {
        'image':image,
        'comments':comments,
    }
    return HttpResponse (template.render(context, request))


def gallery(request):
    latest_images_list = Image.objects.order_by('-receive_date')[:5]
    template = loader.get_template('sstvgallery/gallery.html')
    context = {
        'latest_images_list': latest_images_list,
    }
    return HttpResponse(template.render(context, request))

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all().order_by('receive_date')
    serializer_class = ImageSerializer

    @action(detail=False)
    def most_recent(self, request):
        recent_image = Image.objects.order_by('-receive_date').first()
        serializer = self.get_serializer(recent_image)
        return Response(serializer.data)

    def post(self, request):
        try:
            file = request.data['image']
        except KeyError:
            raise ParseError('Image file missing from request')
        image = Image.objects.create(photo=file, receive_date=datetime.datetime.now())
        return HttpResponse(json.dumps({'message':'image upload success'}), status=200)

