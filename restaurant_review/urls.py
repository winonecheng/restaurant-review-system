from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('restaurants.urls')),
    path('api/', include('reviews.urls')),
    path('api/auth/', include('users.urls')),
]
