import django_filters
from rest_framework import viewsets

from product.permissions import IsAuthorOrIsAdmin, IsAuthor, IsAdminUser
from review.models import Review
from review.serializers import ReviewListSerializer
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filter
from rest_framework.permissions import IsAuthenticated


class ReviewFilter(filters.FilterSet):
    django_filters.CharFilter()

    class Meta:
        model = Review
        fields = ('user', 'product', 'text')


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    # permission_classes = [IsAuthorOrIsAdmin, IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filter.SearchFilter,
                       rest_filter.OrderingFilter]

    filterset_class = ReviewFilter
    search_fields = ['text']
    ordering_fields = ['user', 'product']

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer
        elif self.action == 'retrieve':
            return ReviewListSerializer
        return ReviewListSerializer

    def get_permissions(self):
        print(self.action, '111111111111111')
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'list':
            return []
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        elif self.action == 'destroy':
            return [IsAuthorOrIsAdmin]
        else:
            return []
