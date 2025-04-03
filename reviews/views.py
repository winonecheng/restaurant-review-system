from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for reviews that allows authenticated users to create reviews
    and allows anyone to view reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # Change the permission_classes to allow reading for anonymous users
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['comment']

    def get_queryset(self):
        """
        Optionally filters the reviews by restaurant_id or user_id
        if provided in query params
        """
        queryset = Review.objects.all()
        restaurant_id = self.request.query_params.get('restaurant_id')
        user_id = self.request.query_params.get('user_id')
        
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
