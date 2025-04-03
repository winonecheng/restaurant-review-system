from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Restaurant
from reviews.models import Review

class RestaurantModelTests(TestCase):
    def test_average_score(self):
        """Test that average_score property calculates correctly"""
        # Create test user
        user = User.objects.create_user(username='testuser', password='testpass123')
        
        # Create a restaurant
        restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test St',
            cuisine_type='Italian'
        )
        
        # Create reviews
        Review.objects.create(restaurant=restaurant, user=user, score=4, comment='Good')
        Review.objects.create(restaurant=restaurant, user=user, score=2, comment='Okay')
        
        # Test average calculation
        self.assertEqual(restaurant.average_score, 3.0)

class RestaurantAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.restaurant_data = {
            'name': 'New Restaurant',
            'address': '456 Test Ave',
            'cuisine_type': 'Chinese'
        }
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant', 
            address='123 Test St',
            cuisine_type='Italian'
        )
        self.url = reverse('restaurant-list')
        self.detail_url = reverse('restaurant-detail', args=[self.restaurant.id])

    def test_get_restaurants(self):
        """Test retrieving a list of restaurants"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_restaurant_authenticated(self):
        """Test creating a restaurant when authenticated"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.restaurant_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 2)

    def test_create_restaurant_unauthenticated(self):
        """Test creating a restaurant when unauthenticated fails"""
        response = self.client.post(self.url, self.restaurant_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Restaurant.objects.count(), 1)

    def test_filter_by_cuisine_type(self):
        """Test filtering restaurants by cuisine type"""
        Restaurant.objects.create(
            name='Another Restaurant', 
            address='789 Test Blvd',
            cuisine_type='Chinese'
        )
        response = self.client.get(f"{self.url}?cuisine_type=Italian")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Restaurant')