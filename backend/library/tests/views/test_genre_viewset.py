from django.test import TestCase
from django.urls import reverse
from utils.load_test_data import get_test_data, get_admin_token, get_user_token
from rest_framework import status
from library import models
from library.tests.views.interface_test import ModelTestInterface

class GenresViewSetTest(TestCase, ModelTestInterface):
    @classmethod
    def setUpTestData(cls):
        users = get_test_data('users')
        for item in users:
            models.LibraryMember.objects.create_user(**item)
        models.LibraryMember.objects.create_superuser(
            username='admin', password='admin')
        genres = get_test_data('genres')
        for item in genres:
            models.Genre.objects.create(**item)
    
    @classmethod
    def tearDownClass(cls):
        models.LibraryMember.objects.all().delete()
    
    def test_get_object_list(self):
        response = self.client.get(
            path=reverse('genres-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertIn('count', data)
        self.assertEqual(data['count'], 16)
        result = data.get('results')
        fields = ['id', 'name']
        genre1 = result[0]
        self.assertListEqual(list(genre1.keys()), fields)

    def test_get_object_detail(self):
        response = self.client.get(
            path=reverse('genres-detail', kwargs={"pk":1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        res_payload = response.json()
        fields = ['id', 'name']
        self.assertListEqual(list(res_payload.keys()), fields)
    
    def test_get_non_existent_object(self):
        response = self.client.get(
            path=reverse('genres-detail', kwargs={"pk": 0})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_create_object(self):
        access_token = get_admin_token(self)
        response = self.client.post(
            path=reverse('genres-list'),
            content_type='application/json',
            data={'name': 'Horror'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            path=reverse('genres-list'),
            content_type='application/json',
            data={'name': 'Epic'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(
            path=reverse('genres-list'),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_normal_user_create_object(self):
        access_token = get_user_token(self)
        response = self.client.post(
            path=reverse('genres-list'),
            content_type='application/json',
            data={'name': 'Epic'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)    
    
    def test_unauthenticated_user_create_object(self):
        response = self.client.post(
            path=reverse('genres-list'),
            content_type='application/json',
            data={'name': 'Epic'},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_update_object(self):
        access_token = get_admin_token(self)
        response = self.client.put(
            path=reverse('genres-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={'name': 'Epic'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data, {"id":1, "name": 'Epic'})
        new_detail = self.client.get(path=reverse('genres-detail', kwargs={"pk": 1})).json()
        self.assertEqual(data, new_detail)
        response = self.client.put(
            path=reverse('genres-detail', kwargs={"pk": 1}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_admin_update_non_existent_object(self):
        access_token = get_admin_token(self)
        response = self.client.put(
            path=reverse('genres-detail', kwargs={"pk": 90}),
            content_type='application/json',
            data={'name': 'Epic'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    
    def test_normal_user_update_object(self):
        access_token = get_user_token(self)
        response = self.client.put(
            path=reverse('genres-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={'name': 'Epic'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_update_object(self):
        response = self.client.put(
            path=reverse('genres-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={'name': 'Epic'},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_admin_patch_object(self):
        access_token = get_admin_token(self)
        response = self.client.patch(
            path=reverse('genres-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={'name': 'Epic'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        new_detail = self.client.get(reverse('genres-detail', kwargs={"pk": 1})).json()
        self.assertEqual(data, new_detail)
        response = self.client.patch(
            path=reverse('genres-detail', kwargs={"pk": 1}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        new_detail = self.client.get(reverse('genres-detail', kwargs={"pk": 1})).json()
        self.assertEqual(data, new_detail)
    
    def test_normal_user_patch_object(self):
        access_token = get_user_token(self)
        response = self.client.patch(
            path=reverse('genres-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={'name': 'Epic'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_user_patch_object(self):
        response = self.client.patch(
            path=reverse('genres-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={'name': 'Epic'},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_admin_delete_object(self):
        access_token = get_admin_token(self)
        response = self.client.delete(
            path=reverse('genres-detail', kwargs={"pk": 1}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete(
            path=reverse('genres-detail', kwargs={"pk": 1}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_normal_user_delete_object(self):
        access_token = get_user_token(self)
        response = self.client.delete(
            path=reverse('genres-detail', kwargs={"pk": 1}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_unauthenticated_user_delete_object(self):
        response = self.client.delete(
            path=reverse('genres-detail', kwargs={"pk":1}),
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
    
    