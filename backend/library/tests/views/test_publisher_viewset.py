from django.test import TestCase
from django.urls import reverse
from utils.load_test_data import get_test_data, get_admin_token, get_user_token
from rest_framework import status
from library import models
from library.tests.views.interface_test import ModelTestInterface


class PublishersViewSetTest(ModelTestInterface, TestCase):
    @classmethod
    def setUpTestData(cls):
        users = get_test_data('users')
        for item in users:
            models.LibraryMember.objects.create_user(**item)
        models.LibraryMember.objects.create_superuser(
            username='admin', password='admin')
        publishers = get_test_data('publishers')
        for item in publishers:
            models.Publisher.objects.create(**item)

    
    @classmethod
    def tearDownClass(cls):
        models.LibraryMember.objects.all().delete()
        models.Publisher.objects.all().delete()


    def test_get_object_list(self):
        response = self.client.get(
            path=reverse('publishers-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertIn('count', data)
        self.assertEqual(data['count'], 3)
        result = data.get('results')
        publisher1 = result[0]
        fields = ['id', 'name', 'location']
        self.assertListEqual(list(publisher1.keys()), fields)

    def test_get_object_detail(self):
        res = self.client.get(
            path=reverse('publishers-detail', kwargs={'pk': 1})
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        expected = {
            "id": 1,
            "name": "O’Reilly Media, Inc.",
            "location": "1005 Gravenstein Highway North, Sebastopol, CA 95472"
        }
        self.assertEqual(data, expected)

    def test_get_non_existent_object(self):
        res = self.client.get(
            path=reverse('publishers-detail', kwargs={'pk': 300})
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_create_object(self):
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('publishers-list'),
            content_type='application/json',
            data={'name': 'Online Publisher'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        data = res.json()
        res = self.client.get(
            path=reverse('publishers-detail', kwargs={"pk": data.get('id')})
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(data, res.json())

        res = self.client.post(
            path=reverse('publishers-list'),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_normal_user_create_object(self):
        access_token = get_user_token(self)
        res = self.client.post(
            path=reverse('publishers-list'),
            content_type='application/json',
            data={'name': 'Online Publisher'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_create_object(self):
        res = self.client.post(
            path=reverse('publishers-list'),
            content_type='application/json',
            data={'name': 'Online Publisher'}
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_update_object(self):
        access_token = get_admin_token(self)
        res = self.client.put(
            path=reverse('publishers-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={'location': 'Epic'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = self.client.put(
            path=reverse('publishers-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={'name': 'Online Publisher'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        expected = {'id': 1,'name': 'Online Publisher', "location": None}
        self.assertEqual(data, expected)

    def test_normal_user_update_object(self):
        access_token = get_user_token(self)
        res = self.client.put(
            path=reverse('publishers-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={'name': 'Online Publisher'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_update_object(self):
        res = self.client.put(
            path=reverse('publishers-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={'name': 'Online Publisher'},
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_patch_object(self):
        access_token = get_admin_token(self)
        res = self.client.patch(
            path=reverse('publishers-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={'name': 'Online Publisher'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        old_data = self.client.get(path=reverse('publishers-detail', kwargs={"pk": 1})).json()
        self.assertEqual(data, old_data)

        res = self.client.patch(
            path=reverse('publishers-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_normal_user_patch_object(self):
        access_token = get_user_token(self)
        res = self.client.patch(
            path=reverse('publishers-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={'name': 'Online Publisher'},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_patch_object(self):
        res = self.client.patch(
            path=reverse('publishers-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data={'name': 'Online Publisher'},
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_delete_object(self):
        access_token = get_admin_token(self)
        res = self.client.delete(
            path=reverse('publishers-detail', kwargs={"pk": 1}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        res = self.client.delete(
            path=reverse('publishers-detail', kwargs={"pk": 91}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_normal_user_delete_object(self):
        access_token = get_user_token(self)
        res = self.client.delete(
            path=reverse('publishers-detail', kwargs={"pk": 1}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_delete_object(self):
        res = self.client.delete(
            path=reverse('publishers-detail', kwargs={"pk": 1}),
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)