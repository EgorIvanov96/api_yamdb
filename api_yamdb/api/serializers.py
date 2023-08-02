from rest_framework import serializers

from review.models import Titles, Category, Genre
import datetime as dt


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('name', 'year', 'rating', 'description', 'genre', 'category')
        model = Titles

    def validate_year(self, value):
        year_now = dt.date.today().year
        if value <= year_now:
            raise serializers.ValidationError('Год выпуска не может быть больше текущего года!')
        return value
        

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        # lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre