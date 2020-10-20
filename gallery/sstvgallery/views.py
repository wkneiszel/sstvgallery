from .models import Image, Comment
from .serializers import ImageSerializer
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.urls import reverse
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
import datetime
import json
import random

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
    image_list = Image.objects.order_by('-receive_date').all()
    paginator = Paginator(image_list, 12)
    image_page = paginator.get_page(1)
    template = loader.get_template('sstvgallery/gallery.html')
    context = {
        'image_page': image_page,
        'sorting': "newest",
        'images_per_page': "12",
        'date_start': "",
        'date_end': "",
    }
    return HttpResponse(template.render(context, request))

def sort(request):
    sort_by = request.GET['sorting'] or 'newest'
    images_per_page = int(request.GET['images_per_page'])
    date_start = request.GET['date_start'] or '1999-04-11'
    date_end = request.GET['date_end'] or '3000-01-01'
    page = request.GET['page'] or 1
    if sort_by == 'newest':
        image_list = Image.objects.order_by('-receive_date').filter(receive_date__range=[date_start, date_end]).all()
    elif sort_by == 'oldest': 
        image_list = Image.objects.order_by('receive_date').filter(receive_date__range=[date_start, date_end]).all()
    elif sort_by == 'top': 
        image_list = Image.objects.order_by('-rating').filter(receive_date__range=[date_start, date_end]).all()
    elif sort_by == 'bottom': 
        image_list = Image.objects.order_by('rating').filter(receive_date__range=[date_start, date_end]).all()
    elif sort_by == 'most_comments': 
        image_list = Image.objects.all().annotate(num_comments=Count('comment')).order_by('-num_comments').filter(receive_date__range=[date_start, date_end]).all()
    elif sort_by == 'least_comments': 
        image_list = Image.objects.all().annotate(num_comments=Count('comment')).order_by('num_comments').filter(receive_date__range=[date_start, date_end]).all()
    else:
        image_list = Image.objects.order_by('-receive_date').filter(receive_date__range=[date_start, date_end]).all()
    
    paginator = Paginator(image_list, images_per_page)
    image_page = paginator.get_page(page)

    template = loader.get_template('sstvgallery/gallery.html')
    context = {
        'image_page': image_page,
        'sorting': sort_by,
        'images_per_page': images_per_page,
        'date_start': date_start,
        'date_end': date_end,
    }
    return HttpResponse(template.render(context, request))

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all().order_by('receive_date')
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False)
    def most_recent(self, request):
        recent_image = Image.objects.order_by('-receive_date').first()
        serializer = self.get_serializer(recent_image)
        return Response(serializer.data)

    @action(detail=False)
    def random(self, request):
        images = Image.objects.all()
        random_image = random.choice(images)
        serializer = self.get_serializer(random_image)
        return Response(serializer.data)
        