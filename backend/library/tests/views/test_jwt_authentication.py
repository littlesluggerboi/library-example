from django.test import TestCase
from rest_framework import status
from library.models import LibraryMember
from django.urls import reverse
from utils.load_test_data import get_test_data


class JWTAuthenticationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        library_members = get_test_data('users')
        for member in library_members:
            LibraryMember.objects.create_user(**member)

    @classmethod
    def tearDownClass(cls):
        LibraryMember.objects.all().delete()

    def test_get_api_token(self):
        response = self.client.post(
            content_type='application/json',
            data={"username": "user1", "password": "test"},
            path=reverse('obtain_token')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)

    def test_get_api_token_incorrect_credentials(self):
        response = self.client.post(
            content_type='application/json',
            path=reverse('obtain_token')
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.get(reverse('obtain_token'))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.post(
            content_type='application/json',
            data={"username": "user1", "password": "wrongpassword"},
            path=reverse('obtain_token')
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refreshing_api_token(self):
        response = self.client.post(
            content_type='application/json',
            data={"username": "user1", "password": "test"},
            path=reverse('obtain_token')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh_token = response.json()['refresh']
        response = self.client.post(
            path=reverse('token_refresh'),
            data={"refresh": refresh_token},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('access', data)

    def test_invalid_refresh_token(self):
        response = self.client.post(
            path=reverse('token_refresh'),
            data={"refresh": "Invalid refresh toke"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
