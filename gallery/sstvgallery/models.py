from django.db import models
from django.db.models import Count, Model
from django.core.paginator import Paginator

# Create your models here.
class Image(models.Model):
    photo = models.ImageField('SSTV Image', upload_to='received_images')
    receive_date = models.DateTimeField('Date Received')
    votes = models.IntegerField('Vote Count', default=0)
    rating = models.DecimalField('Average Rating', max_digits=4, decimal_places=2, default=0)

    def __str__(self):
        name = "(" + str(self.pk) + ") " + self.photo.name
        return name

    # Adds the new vote to the average rating of the image.
    def vote(self, new_vote):
        if (new_vote < 1 or new_vote > 10):
            return self.rating
        else:
            self.votes = self.votes + 1
            self.rating = (self.rating*(self.votes-1)+new_vote)/self.votes
            return self.rating
    
    # Get a gallery page containing a filtered, sorted set of images
    @classmethod
    def get_page(cls, sort_by='newest', date_start='1999-04-11', date_end='3000-01-01', images_per_page=12, page_number=1):
        if sort_by == 'newest':
            image_list = cls.objects.order_by('-receive_date').filter(receive_date__range=[date_start, date_end]).all()
        elif sort_by == 'oldest': 
            image_list = cls.objects.order_by('receive_date').filter(receive_date__range=[date_start, date_end]).all()
        elif sort_by == 'top': 
            image_list = cls.objects.order_by('-rating').filter(receive_date__range=[date_start, date_end]).all()
        elif sort_by == 'bottom': 
            image_list = cls.objects.order_by('rating').filter(receive_date__range=[date_start, date_end]).all()
        elif sort_by == 'most_comments': 
            image_list = cls.objects.all().annotate(num_comments=Count('comment')).order_by('-num_comments').filter(receive_date__range=[date_start, date_end]).all()
        elif sort_by == 'least_comments': 
            image_list = cls.objects.all().annotate(num_comments=Count('comment')).order_by('num_comments').filter(receive_date__range=[date_start, date_end]).all()
        else:
            image_list = cls.objects.order_by('-receive_date').filter(receive_date__range=[date_start, date_end]).all()
        
        paginator = Paginator(image_list, images_per_page)
        return paginator.get_page(page_number)


class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    commentor = models.CharField(max_length=50, default="Anonymous")
    comment_text = models.TextField('Comment Text')
    comment_date = models.DateTimeField('Date Posted')

    def __str__(self):
        name = self.commentor + " at " + str(self.comment_date)
        return name
