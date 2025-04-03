from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        restaurant_id = self.request.query_params.get('restaurant_id')
        user_id = self.request.query_params.get('user_id')
        
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
            
        return queryset
