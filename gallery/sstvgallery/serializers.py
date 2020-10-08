from rest_framework import serializers
from .models import Image
from datetime import datetime

class ImageSerializer(serializers.Serializer):
    photo = serializers.ImageField(required=True)
    receive_date = serializers.DateTimeField(read_only=True)
    votes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True) 

    def create(self, validated_data):
        return Image.objects.create(photo=validated_data["photo"], receive_date=datetime.now())
