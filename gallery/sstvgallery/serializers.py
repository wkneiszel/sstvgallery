from rest_framework import serializers

from .models import Image

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('photo', 'receive_date')