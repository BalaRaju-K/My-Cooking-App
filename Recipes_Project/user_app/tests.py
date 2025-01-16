from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

from rest_framework.authtoken.models import Token  
from django.contrib.auth.models import User

class RegisterTestCase(APITestCase):
    def test_register(self):
        data= {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'test123',
            'password2': 'test123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='test123')
        self.token = Token.objects.create(user=self.user)
    
    def test_login(self):
        data = {
            'username': 'testuser',
            'password': 'test123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
