from django.db import models

# Create your models here.
class Image(models.Model):
    photo = models.ImageField('SSTV Image')
    receive_date = models.DateTimeField('Date Received')

class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment_text = models.TextField('Comment Text')
    comment_date = models.DateTimeField('Date Posted')
