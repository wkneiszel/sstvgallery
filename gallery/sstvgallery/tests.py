import datetime

from django.test import TestCase
from rest_framework.test import APIClient
from django.utils import timezone

from .models import Image, Comment
import tempfile
from django.core.files import File
import datetime
import random
from random import randint
# Create your tests here.

class ImageModelTests(TestCase):
    def setUp(self):
        image = tempfile.NamedTemporaryFile(suffix=".png").name
        Image.objects.create(photo=image, receive_date="2020-01-01 12:00:00.00000")

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