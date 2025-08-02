from django.test import TestCase
from library import models
from utils.load_test_data import get_admin_token, get_test_data, get_user_token
from library.tests.views.interface_test import ModelTestInterface
from django.urls import reverse
from rest_framework import status


class BooksViewSetTests(TestCase, ModelTestInterface):
    @classmethod
    def setUpTestData(cls):
        users = get_test_data('users')
        for item in users:
            models.LibraryMember.objects.create_user(**item)
        models.LibraryMember.objects.create_superuser(
            username='admin', password='admin')
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

    def test_get_object_list(self):
        """
        Authenticated and unauthenticated users can get the list of all books
        GET /books
        """
        res = self.client.get(
            path=reverse('books-list'),
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_payload = res.json()
        self.assertIn('results', res_payload)
        self.assertIn('count', res_payload)
        self.assertEqual(res_payload['count'], 4)
        results = res_payload['results']
        result_schema = list(results[0].keys())
        expected_schema = ['genre', 'authors', 'publisher',
                           'language', 'title', 'summary', 'publication_date', 'isbn']
        self.assertSetEqual(set(result_schema), set(expected_schema))

    def test_get_object_detail(self):
        """
        Authenticated and unauthenticated users can get a detail of the books
        GET /books/id
        """
        res = self.client.get(
            path=reverse('books-detail', kwargs={"pk": 1}),
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        schema = list(data.keys())
        fields = ['title', 'summary', 'isbn', 'language',
                  'authors', 'genre', 'publisher', 'publication_date', 'copies']
        self.assertListEqual(schema, fields)

    def test_admin_create_object(self):
        """
        Admin can create books
        POST /books
        """
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [2, 3],
            'genre': [1, 8],
            'copies': 3
        }
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('books-list'),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_payload = res.json()
        schema = list(res_payload.keys())
        fields = ['title', 'summary', 'isbn', 'language',
                  'authors', 'genre', 'publisher', 'publication_date', 'copies']
        self.assertListEqual(schema, fields)

    def test_create_object_missing_fields(self):
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [2, 3],
            'genre': [1, 8],
            # 'copies': 3
        }
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('books-list'),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_object_non_integer_values(self):
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': ['asfqwer', 3],
            'genre': [1, -1],
            'copies': 3
        }
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('books-list'),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_object_non_existent_fk(self):
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [10, 3],
            'genre': [1, 8],
            'copies': 3
        }
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('books-list'),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_object_repeating_fk(self):
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [2, 3],
            'genre': [1, 1],
            'copies': 3
        }
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('books-list'),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_object_missing_not_required_fields(self):
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            # 'publication_date': '1997-08-19',
            # 'publisher': 1,
            'authors': [2, 3],
            'genre': [1, 8],
            'copies': 3
        }
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('books-list'),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_object_empty_fk(self):
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [],
            'genre': [],
            'copies': 3
        }
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('books-list'),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_normal_user_create_object(self):
        """
        Authenticated users are not allowed to add books to the library
        POST /books
        """
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [2, 3],
            'genre': [1, 8],
            'copies': 3
        }
        access_token = get_user_token(self)
        res = self.client.post(
            path=reverse('books-list'),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_create_object(self):
        """
        Unuathenticated users are not allowed to add books to the library
        POST /books
        """
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [2, 3],
            'genre': [1, 8],
            # 'copies': 3
        }
        res = self.client.post(
            path=reverse('books-list'),
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_update_object(self):
        """
        Admin can perform a put operation on an existing book
        PUT /books/id
        """
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [2, 3],
            'genre': [1, 8],
        }
        access_token = get_admin_token(self)
        res = self.client.put(
            path=reverse('books-detail', kwargs={'pk': 1}),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_object_missing_required_fields(self):
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            # 'authors': [2, 3],
            'genre': [1, 8],
        }
        access_token = get_admin_token(self)
        res = self.client.put(
            path=reverse('books-detail', kwargs={'pk': 1}),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_object_missing_non_required_fields(self):
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            # 'publication_date': '1997-08-19',
            # 'publisher': 1,
            'authors': [2, 3],
            'genre': [1, 8],
        }
        access_token = get_admin_token(self)
        res = self.client.put(
            path=reverse('books-detail', kwargs={'pk': 1}),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_object_sending_empty_list(self):
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [],
            'genre': [],
        }
        access_token = get_admin_token(self)
        res = self.client.put(
            path=reverse('books-detail', kwargs={'pk': 1}),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_normal_user_update_object(self):
        """
        Authenticated users are forbidden to perform a put operation on a book
        PUT /books/id
        """
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [2, 3],
            'genre': [1, 8],
        }
        access_token = get_user_token(self)
        res = self.client.put(
            path=reverse('books-detail', kwargs={'pk': 1}),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_update_object(self):
        """
        Unauthenticated users are unauthorized to perform a put operation on a book
        PUT /books/id
        """
        data = {
            'title': 'newbook',
            'summary': 'summary of new book',
            'isbn': '1234567890123',
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [2, 3],
            'genre': [1, 8],
        }
        res = self.client.put(
            path=reverse('books-detail', kwargs={'pk': 1}),
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_patch_object(self):
        """
        Admin is allowed to perform a patch on a book
        PATCH /books/id
        """
        data = {
            "title": "new title",
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [2, 3],
            'genre': [1, 8],
        }
        access_token = get_admin_token(self)
        res = self.client.patch(
            path=reverse('books-detail', kwargs={'pk': 1}),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        actual = res.json()
        expected = {'title': 'new title', 'summary': 'The story follows the experiences of seven children terrorized by It (otherwise known as Pennywise), an evil entity that exploits the fears of its victims to disguise itself while hunting its prey.', 'isbn': '0670813028', 'language': 'English', 'authors': [
            'Shakespeare, William', 'Rowling, Joanne'], 'genre': ['Horror', 'Historical Fiction'], 'publisher': 'O’Reilly Media, Inc.', 'publication_date': '1997-08-19'}
        self.assertDictEqual(actual, expected)

    def test_patch_object_empty_payload(self):
        data = {
        }
        access_token = get_admin_token(self)
        res = self.client.patch(
            path=reverse('books-detail', kwargs={'pk': 1}),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        actual = res.json()
        expected = {'title': 'It', 'summary': 'The story follows the experiences of seven children terrorized by It (otherwise known as Pennywise), an evil entity that exploits the fears of its victims to disguise itself while hunting its prey.', 'isbn': '0670813028', 'language': 'English', 'authors': [
            'King, Stephen E.'], 'genre': ['Horror', 'Novel', 'Thriller', 'Dark Fantasy', 'Coming-of-age story'], 'publisher': 'Viking Press', 'publication_date': "1986-09-15"}
        self.assertDictEqual(actual, expected)

    def test_patch_object_empty_list_genre(self):
        data = {
            'genre': [],
        }
        access_token = get_admin_token(self)
        res = self.client.patch(
            path=reverse('books-detail', kwargs={'pk': 1}),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        actual = res.json()
        expected = {'title': 'It', 'summary': 'The story follows the experiences of seven children terrorized by It (otherwise known as Pennywise), an evil entity that exploits the fears of its victims to disguise itself while hunting its prey.', 'isbn': '0670813028', 'language': 'English', 'authors': [
            'King, Stephen E.'], 'genre': [], 'publisher': 'Viking Press', 'publication_date': "1986-09-15"}
        self.assertDictEqual(actual, expected)

    def test_patch_object_empty_list_authors(self):
        data = {
            'authors': [],
        }
        access_token = get_admin_token(self)
        res = self.client.patch(
            path=reverse('books-detail', kwargs={'pk': 1}),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        actual = res.json()
        expected = {'title': 'It', 'summary': 'The story follows the experiences of seven children terrorized by It (otherwise known as Pennywise), an evil entity that exploits the fears of its victims to disguise itself while hunting its prey.', 'isbn': '0670813028', 'language': 'English', 'authors': [
        ], 'genre': ['Horror', 'Novel', 'Thriller', 'Dark Fantasy', 'Coming-of-age story'], 'publisher': 'Viking Press', 'publication_date': "1986-09-15"}
        self.assertDictEqual(actual, expected)

    def test_normal_user_patch_object(self):
        """
        Authenticated users are forbidden to perform a patch operation on a book
        PATCH /books/id
        """
        data = {
            "title": "new title",
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [2, 3],
            'genre': [1, 8],
        }
        access_token = get_user_token(self)
        res = self.client.patch(
            path=reverse('books-detail', kwargs={'pk': 1}),
            headers={'Authorization': f"Bearer {access_token}"},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_patch_object(self):
        """
        Unauthenticated users are unauthorized to perform a patch operation on a book
        PATCH /books/id
        """
        data = {
            "title": "new title",
            'language': 1,
            'publication_date': '1997-08-19',
            'publisher': 1,
            'authors': [2, 3],
            'genre': [1, 8],
        }
        res = self.client.patch(
            path=reverse('books-detail', kwargs={'pk': 1}),
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_delete_object(self):
        """
        Delete operation is not allowed
        DELETE /books/id
        """
        access_token = get_admin_token(self)
        res = self.client.delete(
            path=reverse('books-detail', kwargs={"pk": 1}),
            headers={'Authorization': f"Bearer {access_token}"}
        )
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_normal_user_delete_object(self):
        """
        authorized users are forbidden to delete a book
        DELETE /books/id
        """
        access_token = get_user_token(self)
        res = self.client.delete(
            path=reverse('books-detail', kwargs={"pk": 1}),
            headers={'Authorization': f"Bearer {access_token}"}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_delete_object(self):
        """
        Unauthorized users are not authorized to delete a book
        DELETE /books/id
        """
        res = self.client.delete(
            path=reverse('books-detail', kwargs={"pk": 1}),
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
