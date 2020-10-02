from django.db import models
from django.db.models import Model

# Create your models here.
class Image(models.Model):
    photo = models.ImageField('SSTV Image', upload_to='received_images')
    receive_date = models.DateTimeField('Date Received')
    votes = models.IntegerField('Vote Count', default=0)
    rating = models.DecimalField('Average Rating', max_digits=4, decimal_places=2, default=0)

class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    commentor = models.CharField(max_length=50, default="Anonymous")
    comment_text = models.TextField('Comment Text')
    comment_date = models.DateTimeField('Date Posted')
