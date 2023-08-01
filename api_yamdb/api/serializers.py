from rest_framework import serializers

from review.models import Titles, Review


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'category', 'genre', 'name', 'year'
        model = Titles

    def get_fields(self):
        fields = super().get_fields()
        if self.context['view'].action == 'retrieve':
            fields['rating'] = serializers.SerializerMethodField()
        return fields

    def get_rating(self, obj):
        reviews = Review.objects.values('score')
        scores = [review['score'] for review in reviews]
        average_rating = math.ceil(sum(scores) / len(scores) if scores else 0)
        return average_rating
