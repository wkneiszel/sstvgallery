from django.db import models
from django.db.models import Model

# Create your models here.
class Image(models.Model):
    photo = models.ImageField('SSTV Image', upload_to='received_images')
    receive_date = models.DateTimeField('Date Received')

class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    commentor = models.CharField(max_length=50, default="Anonymous")
    comment_text = models.TextField('Comment Text')
    comment_date = models.DateTimeField('Date Posted')
