from rest_framework import serializers

from review.models import Titles


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        scores = [review.score for review in reviews]
        average_rating = sum(scores) / len(scores) if scores else 0
        return average_rating

    class Meta:
        fields = '__all__'
        model = Titles
