from rest_framework import viewsets
from .serializers import CommentsSerializer

from review.models import Comments, Review


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        return Comments.objects.filter(review=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs['review_id']
        review = Review.objects.get(id=review_id)
        serializer.save(author=self.request.user,
                        review=review)