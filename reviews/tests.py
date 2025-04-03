from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from restaurants.models import Restaurant
from .models import Review

class ReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test St',
            cuisine_type='Italian'
        )
        
    def test_review_creation(self):
        """Test that a review can be created and properly related to user and restaurant"""
        review = Review.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            score=4,
            comment='Great food!'
        )
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.restaurant, self.restaurant)
        self.assertEqual(str(review), 'testuser - Test Restaurant - 4')

class ReviewAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')
        self.restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test St',
            cuisine_type='Italian'
        )
        self.review = Review.objects.create(
            restaurant=self.restaurant,
            user=self.user,
            score=4,
            comment='Great food!'
        )
        self.url = reverse('review-list')
        self.detail_url = reverse('review-detail', args=[self.review.id])
        self.review_data = {
            'restaurant': self.restaurant.id,
            'score': 5,
            'comment': 'Amazing experience!'
        }

    def test_get_reviews(self):
        """Test retrieving a list of reviews"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_review_authenticated(self):
        """Test creating a review when authenticated"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.review_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        
    def test_create_review_unauthenticated(self):
        """Test creating a review when unauthenticated fails"""
        response = self.client.post(self.url, self.review_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_update_own_review(self):
        """Test updating own review"""
        self.client.force_authenticate(user=self.user)
        update_data = {'score': 3, 'comment': 'Updated opinion'}
        response = self.client.patch(self.detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.review.refresh_from_db()
        self.assertEqual(self.review.score, 3)
        
    def test_update_others_review_fails(self):
        """Test that updating another user's review fails"""
        self.client.force_authenticate(user=self.other_user)
        update_data = {'score': 1, 'comment': 'Trying to change score'}
        response = self.client.patch(self.detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_filter_by_restaurant(self):
        """Test filtering reviews by restaurant"""
        another_restaurant = Restaurant.objects.create(
            name='Another Restaurant', 
            address='456 Test Ave',
            cuisine_type='Chinese'
        )
        Review.objects.create(
            restaurant=another_restaurant,
            user=self.user,
            score=2,
            comment='Not good'
        )
        
        response = self.client.get(f"{self.url}?restaurant_id={self.restaurant.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['score'], 4)