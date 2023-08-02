import math
import datetime as dt

from rest_framework import serializers


from users.users import User
from review.models import Comments, Review, Titles, Genre, Category


class UserRegistrationSerializer(serializers.Serializer):
    """Регистрация пользователя."""
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.RegexField(max_length=150,
                                      required=True,
                                      regex=r'^[\w.@+-]+$')

    class Meta:
        fields = ('username', 'email',)

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Использование username '
                                              '"me" запрещено!')
        if User.objects.filter(username=data.get('username')) and User.objects.filter(email=data.get('email')):
            return data
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError('Пользователь с таким username '
                                              'уже существует.')

        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError('Пользователь с таким email '
                                              'уже существует.')
        return data


class TokenSerializer(serializers.Serializer):
    """Получение токена пользователя."""
    username = serializers.RegexField(regex=r'^[\w.@+-]+$',
                                      max_length=150,
                                      required=True)
    confirmation_code = serializers.CharField(required=True, max_length=150)

    class Meta:
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$',
                                      max_length=150,
                                      required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$',
                                      max_length=150,
                                      required=True)

    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    title = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault(),
        required=False)

    class Meta:
        fields = '__all__'
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    review = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        fields = '__all__'
        model = Comments


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True)
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Titles

    def validate_year(self, value):
        year_now = dt.date.today().year
        if value >= year_now:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего года!')
        return value

    def get_fields(self):
        fields = super().get_fields()
        if self.context['view'].action == 'retrieve':
            fields['id'] = serializers.IntegerField()
            fields['rating'] = serializers.SerializerMethodField()
        elif self.context['view'].action == 'create':
            fields['id'] = serializers.IntegerField(required=False)
        return fields

    def get_rating(self, obj):
        reviews = Review.objects.values('score')
        scores = [review['score'] for review in reviews]
        average_rating = math.ceil(sum(scores) / len(scores) if scores else 0)
        return average_rating


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        # lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
