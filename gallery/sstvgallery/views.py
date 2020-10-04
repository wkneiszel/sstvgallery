from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from rest_framework import viewsets
from .models import Image, Comment
from .serializers import ImageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import datetime
from rest_framework.exceptions import ParseError
import json
from django.urls import reverse
from decimal import Decimal
from django.db.models import Count
# Create your views here.

def about(request):
    template = loader.get_template('sstvgallery/about.html')
    context = {}
    return HttpResponse(template.render(context, request))

def detail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    comments = image.comment_set.order_by('-comment_date')
    template = loader.get_template('sstvgallery/detail.html')
    context = {
        'image':image,
        'comments':comments,
    }
    return HttpResponse(template.render(context, request))

def comment(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    comments = image.comment_set.order_by('-comment_date')
    if request.POST['comment_text']:
        Comment.objects.create(image=image, commentor=(request.POST['commentor'] or "Anonymous"), comment_text=request.POST['comment_text'], comment_date=datetime.datetime.now())
    else:
        return render(request, 'sstvgallery/detail.html', {
            'image': image,
            'comments': comments,
            'error_message': "Comment text cannot be empty",
        })
    return HttpResponseRedirect(reverse('detail', args=(image.id,)))

def vote(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    comments = image.comment_set.order_by('-comment_date')
    if request.POST['rating']:
        image.votes = image.votes + 1
        rating = Decimal(request.POST['rating'])
        image.rating = (image.rating*(image.votes-1)+rating)/image.votes
        image.save()
    else:
        return render(request, 'sstvgallery/detail.html',{
            'image': image,
            'comments': comments,
            'error_message': "Rating cannot be empty",
        })
    return HttpResponseRedirect(reverse('results', args=(image.id,)))

def results(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    comments = image.comment_set.order_by('-comment_date')
    template = loader.get_template('sstvgallery/results.html')
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

def sort(request):
    sort_by = request.GET['sorting']
    if sort_by == 'newest':
        latest_images_list = Image.objects.order_by('-receive_date')[:5]
    elif sort_by == 'oldest': 
        latest_images_list = Image.objects.order_by('receive_date')[:5]
    elif sort_by == 'top': 
        latest_images_list = Image.objects.order_by('-rating')[:5]
    elif sort_by == 'bottom': 
        latest_images_list = Image.objects.order_by('rating')[:5]
    elif sort_by == 'most_comments': 
        latest_images_list = Image.objects.all().annotate(num_comments=Count('comment')).order_by('-num_comments')
    elif sort_by == 'least_comments': 
        latest_images_list = Image.objects.all().annotate(num_comments=Count('comment')).order_by('num_comments')
    else:
        latest_images_list = Image.objects.order_by('-receive_date')[:5]
    template = loader.get_template('sstvgallery/gallery.html')
    context = {
        'latest_images_list': latest_images_list,
        'sorting': sort_by,
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

