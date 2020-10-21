from django.db import models
from django.db.models import Model

# Create your models here.
class Image(models.Model):
    photo = models.ImageField('SSTV Image', upload_to='received_images')
    receive_date = models.DateTimeField('Date Received')
    votes = models.IntegerField('Vote Count', default=0)
    rating = models.DecimalField('Average Rating', max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        name = "(" + str(self.pk) + ") " + self.photo.name
        return name

    def vote(self, new_vote):
        if (new_vote < 1 or new_vote > 10):
            return self.rating
        else:
            self.votes = self.votes + 1
            self.rating = (self.rating*(self.votes-1)+new_vote)/self.votes
            return self.rating

class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    commentor = models.CharField(max_length=50, default="Anonymous")
    comment_text = models.TextField('Comment Text')
    comment_date = models.DateTimeField('Date Posted')

    def __str__(self):
        name = self.commentor + " at " + str(self.comment_date)
        return name
