from django.test import TestCase
from django.urls import reverse
from utils.load_test_data import get_test_data, get_admin_token, get_user_token
from rest_framework import status
from library import models
from library.tests.views.interface_test import ModelTestInterface

class LanguagesViewSetTest(TestCase, ModelTestInterface):
    @classmethod
    def setUpTestData(cls):
        users = get_test_data('users')
        for item in users:
            models.LibraryMember.objects.create_user(**item)
        models.LibraryMember.objects.create_superuser(
            username='admin', password='admin')
        languages = get_test_data('languages')
        for item in languages:
            models.Language.objects.create(**item)
    
    @classmethod
    def tearDownClass(cls):
        models.LibraryMember.objects.all().delete()

    def test_get_object_list(self):
        response = self.client.get(
            path=reverse('languages-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertIn('count', data)
        self.assertEqual(data['count'], 3)
        result = data['results']
        language1 = result[0]
        fields = ['id', 'name']
        self.assertListEqual(list(language1.keys()), fields)
    
    def test_get_object_detail(self):
        response = self.client.get(
            path=reverse('languages-detail', kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        expected = {"id": 1, "name": "English"}
        self.assertEqual(data, expected)

    def test_get_non_existent_object(self):
        response = self.client.get(
            path=reverse('languages-detail', kwargs={"pk": 90})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_create_object(self):
        access_token = get_admin_token(self)
        response = self.client.post(
            path=reverse('languages-list'),
            content_type='application/json',
            headers={'Authorization' : f'Bearer {access_token}'},
            data={'name': 'Aztech'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            path=reverse('languages-list'),
            content_type='application/json',
            headers={'Authorization' : f'Bearer {access_token}'},
            data={}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_normal_user_create_object(self):
        access_token = get_user_token(self)
        response = self.client.post(
            path=reverse('languages-list'),
            content_type='application/json',
            headers={'Authorization' : f'Bearer {access_token}'},
            data={'name': 'Aztech'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_user_create_object(self):
        response = self.client.post(
            path=reverse('languages-list'),
            content_type='application/json',
            data={'name': 'Aztech'}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_update_object(self):
        access_token = get_admin_token(self)
        response = self.client.put(
            path=reverse('languages-detail', kwargs={'pk':1}),
            content_type='application/json',
            headers={'Authorization' : f'Bearer {access_token}'},
            data={'name': 'Aztech'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        new_detail = self.client.get(
            path=reverse('languages-detail', kwargs={'pk': 1})
        ).json()
        self.assertEqual(data, new_detail)
        response = self.client.put(
            path=reverse('languages-detail', kwargs={'pk':1}),
            content_type='application/json',
            headers={'Authorization' : f'Bearer {access_token}'},
            data={}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(
            path=reverse('languages-detail', kwargs={'pk':10}),
            content_type='application/json',
            headers={'Authorization' : f'Bearer {access_token}'},
            data={'name': 'Aztech'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_normal_user_update_object(self):
        access_token = get_user_token(self)
        response = self.client.put(
            path=reverse('languages-detail', kwargs={'pk':1}),
            content_type='application/json',
            headers={'Authorization' : f'Bearer {access_token}'},
            data={'name': 'Aztech'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_user_update_object(self):
        response = self.client.put(
            path=reverse('languages-detail', kwargs={'pk':1}),
            content_type='application/json',
            data={'name': 'Aztech'}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_admin_patch_object(self):
        access_token = get_admin_token(self)
        response = self.client.patch(
            path=reverse('languages-detail', kwargs={'pk':1}),
            content_type='application/json',
            headers={'Authorization' : f'Bearer {access_token}'},
            data={'name': 'Aztech'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        new_detail = self.client.get(
            path=reverse('languages-detail', kwargs={'pk': 1})
        ).json()
        self.assertEqual(data, new_detail)
        response = self.client.patch(
            path=reverse('languages-detail', kwargs={'pk':1}),
            content_type='application/json',
            headers={'Authorization' : f'Bearer {access_token}'},
            data={}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        new_detail = self.client.get(
            path=reverse('languages-detail', kwargs={'pk': 1})
        ).json()
        self.assertEqual(data, new_detail)
    
    
    def test_normal_user_patch_object(self):
        access_token = get_user_token(self)
        response = self.client.patch(
            path=reverse('languages-detail', kwargs={'pk':1}),
            content_type='application/json',
            headers={'Authorization' : f'Bearer {access_token}'},
            data={'name': 'Aztech'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_user_patch_object(self):
        response = self.client.patch(
            path=reverse('languages-detail', kwargs={'pk':1}),
            content_type='application/json',
            data={'name': 'Aztech'}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_admin_delete_object(self):
        access_token = get_admin_token(self)
        response = self.client.delete(
            path=reverse('languages-detail', kwargs={'pk':1}),
            headers={'Authorization' : f'Bearer {access_token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(
            path=reverse('languages-detail', kwargs={'pk':78}),
            headers={'Authorization' : f'Bearer {access_token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_normal_user_delete_object(self):
        access_token = get_user_token(self)
        response = self.client.delete(
            path=reverse('languages-detail', kwargs={'pk':1}),
            headers={'Authorization' : f'Bearer {access_token}'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_user_delete_object(self):
        response = self.client.delete(
            path=reverse('languages-detail', kwargs={'pk':1}),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    