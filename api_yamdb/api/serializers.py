from rest_framework import serializers

from review.models import Titles


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Titles
        