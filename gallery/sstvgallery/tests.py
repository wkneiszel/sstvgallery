from .models import Image, Comment
from django.core.files import File
from django.test import TestCase
from django.utils import timezone
from random import randint
from rest_framework.test import APIClient
import datetime
import datetime
import random
import tempfile
# Create your tests here.

class ImageModelTests(TestCase):
    def setUp(self):
        image = tempfile.NamedTemporaryFile(suffix=".png").name
        Image.objects.create(photo=image, receive_date="2020-01-01 12:00:00.00000")
        Image.objects.create(photo=image, receive_date="2020-01-02 12:00:00.00000")
        Image.objects.create(photo=image, receive_date="2020-01-03 12:00:00.00000")
        Image.objects.create(photo=image, receive_date="2020-01-04 12:00:00.00000")
        Image.objects.create(photo=image, receive_date="2020-01-05 12:00:00.00000")
        Image.objects.create(photo=image, receive_date="2020-01-06 12:00:00.00000")
        Image.objects.create(photo=image, receive_date="2020-01-07 12:00:00.00000")
        Image.objects.create(photo=image, receive_date="2020-01-08 12:00:00.00000")
        Image.objects.create(photo=image, receive_date="2020-01-09 12:00:00.00000")
        Image.objects.create(photo=image, receive_date="2020-01-10 12:00:00.00000")
        Image.objects.create(photo=image, receive_date="2020-01-11 12:00:00.00000")
        Image.objects.create(photo=image, receive_date="2020-01-12 12:00:00.00000")
        Image.objects.create(photo=image, receive_date="2020-01-13 12:00:00.00000")


    def test_vote(self):
        image = Image.objects.get(receive_date="2020-01-01 12:00:00.00000")

        #test an out-of-bounds vote
        self.assertEqual(image.vote(900), 0)
        self.assertEqual(image.votes, 0)
        self.assertEqual(image.rating, 0)

        #test first vote
        self.assertEqual(image.vote(4), 4)
        self.assertEqual(image.rating, 4)
        self.assertEqual(image.votes, 1)

        #test that second vote averages the first two votes
        self.assertEqual(image.vote(8), 6)
        self.assertEqual(image.rating, 6)
        self.assertEqual(image.votes, 2)

        #reset votes
        image.votes = 0
        image.rating = 0

        #test a large number of votes with known values
        for i in range (1, 1001):
            vote = (i % 10) + 1
            image.vote(vote)
        self.assertEqual(image.votes, 1000)
        self.assertEqual(image.rating, 5.5)

        #reset votes
        image.votes = 0
        image.rating = 0

        #test a large number of random values
        random_votes = []
        for i in range (1, 1001):
            vote = randint(1, 10)
            random_votes.append(vote)
            image.vote(vote)
        average = sum(random_votes) / len(random_votes)
        self.assertEqual(image.votes, 1000)
        self.assertAlmostEqual(image.rating, average)

    def test_get_page(self):
        #test sorting
        newest_page = Image.get_page('newest', '2019-01-01 12:00:00.00000', '2021-01-01 12:00:00.00000', 24, 1)
        self.assertEqual(newest_page.object_list[0].receive_date.date(), datetime.date(2020, 1, 13))
        self.assertEqual(newest_page.has_next(), False)
        self.assertEqual(len(newest_page.object_list), 13)
        oldest_page = Image.get_page('oldest', '2019-01-01 12:00:00.00000', '2021-01-01 12:00:00.00000', 24, 1)
        self.assertEqual(oldest_page.object_list[0].receive_date.date(), datetime.date(2020, 1, 1))

        #test page size and pagination
        small_page = Image.get_page('oldest', '2019-01-01 12:00:00.00000', '2021-01-01 12:00:00.00000', 5, 1)
        self.assertEqual(len(small_page.object_list), 5)
        small_page2 = Image.get_page('oldest', '2019-01-01 12:00:00.00000', '2021-01-01 12:00:00.00000', 5, 2)
        self.assertEqual(len(small_page2.object_list), 5)
        self.assertEqual(small_page2.object_list[0].receive_date.date(), datetime.date(2020, 1, 6))

        #test start and end dates
        date_filtered_page = Image.get_page('oldest', '2020-01-05 12:00:00.00000', '2020-01-10 12:00:00.00000', 24, 1)
        self.assertEqual(date_filtered_page.object_list[0].receive_date.date(), datetime.date(2020, 1, 5))
        self.assertEqual(date_filtered_page.object_list[5].receive_date.date(), datetime.date(2020, 1, 10))
        self.assertEqual(len(date_filtered_page.object_list), 6)

        #test default values
        default_page = Image.get_page()
        self.assertEqual(default_page.object_list[0].receive_date.date(), datetime.date(2020, 1, 13))
        self.assertEqual(default_page.has_next(), True)
        self.assertEqual(len(default_page.object_list), 12)