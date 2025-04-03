from rest_framework import viewsets, permissions
from .models import Restaurant
from .serializers import RestaurantSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        cuisine_type = self.request.query_params.get('cuisine_type')
        sort_by_score = self.request.query_params.get('sort_by_score')
        
        if cuisine_type:
            queryset = queryset.filter(cuisine_type=cuisine_type)
            
        if sort_by_score:
            # Simple approach - not efficient for large datasets
            queryset = sorted(queryset, key=lambda x: x.average_score, reverse=True)
            
        return queryset
