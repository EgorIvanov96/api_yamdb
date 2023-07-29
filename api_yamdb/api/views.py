from rest_framework import viewsets

from .serializers import ReviewSerializer
from review.models import Review, Titles


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = Titles.objects.get(id=title_id)
        serializer.save(author=self.request.user,
                        title=title)
