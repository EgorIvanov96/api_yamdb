from django.contrib import admin

from review.models import Comments, Review, Titles, Genre, Category, TitleGenre
from users.users import User


admin.site.register(Titles)
admin.site.register(Comments)
admin.site.register(Review)
admin.site.register(TitleGenre)
admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Category)