from rest_framework import serializers

from review.models import Genre


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Genre