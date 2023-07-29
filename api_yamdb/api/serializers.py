from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from review.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    title = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        fields = '__all__'
        model = Review
