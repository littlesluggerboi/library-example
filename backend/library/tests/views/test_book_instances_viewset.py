from django.test import TestCase
from library import models
from utils.load_test_data import get_admin_token, get_test_data, get_user_token
from django.urls import reverse
from rest_framework import status


class BookInstancesViewSetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        users = get_test_data('users')
        models.LibraryMember.objects.create_superuser(
            username='admin', password='admin')
        for item in users:
            models.LibraryMember.objects.create_user(**item)
        for item in get_test_data('authors'):
            models.Author.objects.create(**item)
        for item in get_test_data('genres'):
            models.Genre.objects.create(**item)
        for item in get_test_data('languages'):
            models.Language.objects.create(**item)
        for item in get_test_data('publishers'):
            models.Publisher.objects.create(**item)
        for item in get_test_data('books'):
            authors = item.pop('authors')
            genres = item.pop('genre')
            language = item.pop('language')
            if language:
                language = models.Language.objects.get(pk=language)
            publisher = item.pop('publisher')
            if publisher:
                publisher = models.Publisher.objects.get(pk=publisher)
            book = models.Book.objects.create(
                **item, language=language, publisher=publisher)
            for author in authors:
                book.authors.add(models.Author.objects.get(pk=author))
            for genre in genres:
                book.genre.add(models.Genre.objects.get(pk=genre))
            book.save()
        for item in get_test_data('book_instances'):
            book = item.pop('book')
            book = models.Book.objects.get(pk=book)
            borrower = item.pop('borrower', None)
            if borrower:
                borrower = models.LibraryMember.objects.get(pk=borrower)
            model_instance = models.BookInstance.objects.create(
                **item, book=book)
            model_instance.borrower = borrower
            model_instance.save()
        for item in get_test_data('book_instance_borrower_records'):
            book_instance = item.pop('book_instance')
            book_instance = models.BookInstance.objects.get(pk=book_instance)
            borrower = item.pop('borrower')
            borrower = models.LibraryMember.objects.get(pk=borrower)
            models.BookInstanceBorrowerRecord.objects.create(
                **item, borrower=borrower, book_instance=book_instance)

    def test_get_list(self):
        res = self.client.get(
            path=reverse('book_instances-list')
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_payload = res.json()
        self.assertIn('results', res_payload)
        self.assertIn('count', res_payload)

    def test_get_instance_detail(self):
        res = self.client.get(
            path=reverse('book_instances-detail', kwargs={'pk': 4})
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_create_instance(self):
        data = {
            'book': 1,
        }
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('book_instances-list'),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res = self.client.get(
            path=reverse('book_instances-detail', kwargs={'pk': 5})
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        book_instance = res.json()
        self.assertEqual(book_instance.get('book_number'), 4)

    def test_missing_field_create_instance(self):
        data = {
        }
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('book_instances-list'),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_non_existent_book_create_instance(self):

        data = {
            'book': 90,
        }
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('book_instances-list'),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_normal_user_create_instance(self):

        data = {
            'book': 1,
        }
        access_token = get_user_token(self)
        res = self.client.post(
            path=reverse('book_instances-list'),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_create_instance(self):

        data = {
            'book': 1,
        }
        res = self.client.post(
            path=reverse('book_instances-list'),
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_instance(self):
        data = {
            'book': 1,
            'status': 'Available',
            'book_number': 3
        }
        access_token = get_admin_token(self)
        res = self.client.put(
            path=reverse('book_instances-detail', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_instance(self):
        data = {
            'book': 1,
            'status': 'Available',
            'book_number': 3
        }
        access_token = get_admin_token(self)
        res = self.client.patch(
            path=reverse('book_instances-detail', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_instance(self):
        access_token = get_admin_token(self)
        res = self.client.delete(
            path=reverse('book_instances-detail', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_admin_borrow_a_book(self):
        # POST /book_instances/1/borrow
        # 204 200
        data = {
            'return_date': '2025-08-15'
        }
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('book_instances-borrow', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.post(
            path=reverse('book_instances-borrow', kwargs={'pk': 4}),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        res = self.client.post(
            path=reverse('book_instances-borrow', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_normal_user_borrow_a_book(self):
        data = {
            'return_date': '2025-08-15'
        }
        access_token = get_user_token(self)
        res = self.client.post(
            path=reverse('book_instances-borrow', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.post(
            path=reverse('book_instances-borrow', kwargs={'pk': 4}),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        res = self.client.post(
            path=reverse('book_instances-borrow', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_user_borrow_a_book(self):
        data = {
            'return_date': '2025-08-15'
        }
        res = self.client.post(
            path=reverse('book_instances-borrow', kwargs={'pk': 1}),
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_disable_book_instance(self):
        access_token = get_admin_token(self)
        res = self.client.get(
            path=reverse('book_instances-disable', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertEqual(data['status'], 'Unavailable')

        res = self.client.get(
            path=reverse('book_instances-disable', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertEqual(data['status'], 'Unavailable')

    def test_admin_disable_book_on_loan(self):
        access_token = get_admin_token(self)
        res = self.client.get(
            path=reverse('book_instances-disable', kwargs={'pk': 4}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_normal_user_disable_book(self):
        access_token = get_user_token(self)
        res = self.client.get(
            path=reverse('book_instances-disable', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_disable_book(self):
        res = self.client.get(
            path=reverse('book_instances-disable', kwargs={'pk': 1}),
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_return_book(self):
        access_token = get_user_token(self)
        res = self.client.get(
            path=reverse('book_instances-return_book', kwargs={'pk': 4}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertEqual(data['status'], 'Available')

    def test_non_borrower_return_book(self):
        access_token = get_admin_token(self)
        res = self.client.get(
            path=reverse('book_instances-return_book', kwargs={'pk': 4}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_user_return_book(self):
        res = self.client.get(
            path=reverse('book_instances-return_book', kwargs={'pk': 4}),
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_return_available_book(self):
        access_token = get_admin_token(self)
        res = self.client.get(
            path=reverse('book_instances-return_book', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_unavailable_book(self):
        access_token = get_admin_token(self)
        res = self.client.get(
            path=reverse('book_instances-return_book', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_get_instance_record(self):
        access_token = get_admin_token(self)
        res = self.client.get(
            path=reverse('book_instances-record', kwargs={'pk': 3}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_normal_user_get_instance_record(self):
        access_token = get_user_token(self)
        res = self.client.get(
            path=reverse('book_instances-record', kwargs={'pk': 3}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_user_get_instance_record(self):
        res = self.client.get(
            path=reverse('book_instances-record', kwargs={'pk': 3}),
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_return_book_record(self):
        access_token = get_user_token(self)
        res = self.client.get(
            path=reverse('book_instances-return_book', kwargs={'pk': 4}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        access_token = get_admin_token(self)
        res = self.client.get(
            path=reverse('book_instances-record', kwargs={'pk': 4}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertEqual(len(data['record']), 1)
