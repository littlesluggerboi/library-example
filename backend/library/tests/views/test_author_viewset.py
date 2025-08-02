from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from utils.load_test_data import get_test_data, get_admin_token, get_user_token
from library import models
from django.utils import timezone
from library.tests.views.interface_test import ModelTestInterface

class AuthorsViewSetTest(TestCase, ModelTestInterface):
    @classmethod
    def setUpTestData(cls):
        users = get_test_data('users')
        for item in users:
            models.LibraryMember.objects.create_user(**item)
        authors = get_test_data('authors')
        models.LibraryMember.objects.create_superuser(
            username='admin', password='admin')
        for item in authors:
            models.Author.objects.create(**item)

    @classmethod
    def tearDownClass(cls):
        models.LibraryMember.objects.all().delete()
        models.Author.objects.all().delete()

    def test_get_object_list(self):
        response = self.client.get(reverse('authors-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('count', data)
        self.assertEqual(data['count'], 3)
        self.assertIn('results', data)
        author1 = data['results'][0]
        fields = ['id', 'first_name', 'last_name',
                  'middle_name', 'date_of_birth', 'date_of_death']
        self.assertListEqual(fields, list(author1.keys()))

    def test_get_object_detail(self):
        response = self.client.get(reverse('authors-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        fields = ['id', 'first_name', 'last_name', 'middle_name',
                  'date_of_birth', 'date_of_death', 'books']
        self.assertListEqual(fields, list(data.keys()))
        expected = get_test_data("authors")[0]
        expected['books'] = []
        expected['id'] = 1
        self.assertDictEqual(data, expected)

    def test_get_non_existent_object(self):
        response = self.client.get(
            reverse('authors-detail', kwargs={'pk': 312}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_create_object(self):
        access_token = get_admin_token(self)
        data = {"first_name": "William", "last_name": "Shakespeare",
                'date_of_birth': '1564-04-23', 'date_of_death': '1616-04-23'}
        response = self.client.post(path=reverse('authors-list'), data=data, content_type='application/json',
                                    headers={'Authorization': f'Bearer {access_token}'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_dod_lt_dob(self):
        access_token = get_admin_token(self)
        data = {"first_name": "William", "last_name": "Shakespeare",
                'date_of_birth': '1564-04-23', 'date_of_death': '1564-04-22'}
        response = self.client.post(path=reverse('authors-list'), data=data, content_type='application/json',
                                    headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dod_gt_today(self):
        access_token = get_admin_token(self)
        data = {"first_name": "William", "last_name": "Shakespeare",
                'date_of_death': (timezone.now() + timezone.timedelta(days=1))}
        response = self.client.post(path=reverse('authors-list'), data=data, content_type='application/json',
                                    headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dob_gt_today(self):
        access_token = get_admin_token(self)
        data = {"first_name": "William", "last_name": "Shakespeare",
                'date_of_birth': (timezone.now() + timezone.timedelta(days=1))}
        response = self.client.post(path=reverse('authors-list'), data=data, content_type='application/json',
                                    headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dob_and_dod_are_omitted(self):
        access_token = get_admin_token(self)
        data = {"first_name": "William", "last_name": "Shakespeare"}
        response = self.client.post(path=reverse('authors-list'), data=data, content_type='application/json',
                                    headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_normal_user_create_object(self):
        access_token = get_user_token(self)
        data = {"first_name": "William", "last_name": "Shakespeare",
                'date_of_birth': '1564-04-23', 'date_of_death': '1616-04-23'}
        response = self.client.post(path=reverse('authors-list'), data=data, content_type='application/json',
                                    headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_create_object(self):
        data = {"first_name": "William", "last_name": "Shakespeare",
                'date_of_birth': '1564-04-23', 'date_of_death': '1616-04-23'}
        response = self.client.post(path=reverse('authors-list'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_update_object(self):
        access_token = get_admin_token(self)
        data = {"first_name": "Willian"}
        response = self.client.put(
            path=reverse('authors-detail',
                         kwargs={"pk": 1}), data=data,
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['last_name'] = "Sphere"
        response = self.client.put(
            path=reverse('authors-detail',
                         kwargs={"pk": 1}), data=data,
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data["id"] = 1
        data['middle_name'] = None
        data['date_of_birth'] = None
        data['date_of_death'] = None
        self.assertDictEqual(response.json(), data)
    
    def test_admin_update_non_existent_object(self):
        access_token = get_admin_token(self)
        data = {"first_name": "Frank", "last_name":"Franky"}
        response = self.client.put(
            path=reverse('authors-detail',kwargs={"pk": 90}),
            data=data,
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_normal_user_update_object(self):
        access_token = get_user_token(self)
        data = {"first_name": "Willian", "last_name": "Shakespeare"}
        response = self.client.patch(
            path=reverse('authors-detail',
                         kwargs={"pk": 1}), data=data,
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_update_object(self):
        data = {"first_name": "Willian", "last_name": "Shakespeare"}
        response = self.client.patch(
            path=reverse('authors-detail',
                         kwargs={"pk": 1}), data=data,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_patch_object(self):
        old_data_response = self.client.get(
            path=reverse('authors-detail', kwargs={"pk": 1})
        )
        self.assertEqual(old_data_response.status_code, status.HTTP_200_OK)
        expected = old_data_response.json()
        expected.pop('books')
        access_token = get_admin_token(self)
        response = self.client.patch(
            path=reverse('authors-detail',
                         kwargs={"pk": 1}), data={'first_name': 'willian'},
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected['first_name'] = 'willian'
        actual = response.json()
        self.assertDictEqual(expected, actual)

    def test_normal_user_patch_object(self):
        old_data = self.client.get(
            reverse('authors-detail', kwargs={"pk": 1}),
        )
        self.assertEqual(old_data.status_code, status.HTTP_200_OK)
        access_token = get_user_token(self)
        patch_payload = {"first_name": "will"}
        response = self.client.patch(
            path=reverse('authors-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data=patch_payload,
            headers={'Authorization': f"Bearer {access_token}"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_patch_object(self):
        patch_payload = {"first_name": "will"}
        response = self.client.patch(
            path=reverse('authors-detail', kwargs={"pk": 1}),
            content_type='application/json',
            data=patch_payload
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_delete_object(self):
        access_token = get_admin_token(self)
        response = self.client.delete(
            path=reverse('authors-detail', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        deleted_author = self.client.get(
            path=reverse('authors-detail', kwargs={'pk': 1})
        )
        self.assertEqual(deleted_author.status_code, status.HTTP_404_NOT_FOUND)

    def test_normal_user_delete_object(self):
        access_token = get_user_token(self)
        response = self.client.delete(
            path=reverse('authors-detail', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_delete_object(self):
        response = self.client.delete(
            path=reverse('authors-detail', kwargs={'pk': 1}),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
