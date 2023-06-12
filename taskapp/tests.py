from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from profiles.models import UserProfile

class UserProfileAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = UserProfile.objects.create(user=self.user, name='John Doe', email='johndoe@example.com')

    def test_create_user_profile_authenticated(self):
        url = reverse('profile-list')
        data = {
            'name': 'Jane Smith',
            'email': 'janesmith@example.com',
            'bio': 'I am a test user.'
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 2)
        self.assertEqual(UserProfile.objects.last().name, 'Jane Smith')

    def test_create_user_profile_unauthenticated(self):
        url = reverse('profile-list')
        data = {
            'name': 'Jane Smith',
            'email': 'janesmith@example.com',
            'bio': 'I am a test user.'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_update_user_profile_authenticated(self):
        url = reverse('profile-detail', args=[self.profile.id])
        data = {
            'name': 'John Johnson',
            'email': 'johnjohnson@example.com',
            'bio': 'Updated bio.'
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserProfile.objects.get(id=self.profile.id).name, 'John Johnson')

    def test_update_user_profile_unauthenticated(self):
        url = reverse('profile-detail', args=[self.profile.id])
        data = {
            'name': 'John Johnson',
            'email': 'johnjohnson@example.com',
            'bio': 'Updated bio.'
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(UserProfile.objects.get(id=self.profile.id).name, 'John Doe')
