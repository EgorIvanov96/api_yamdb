from rest_framework import serializers

from review.models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Category