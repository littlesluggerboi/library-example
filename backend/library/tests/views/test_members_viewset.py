from django.test import TestCase
from django.urls import reverse
from utils.load_test_data import get_test_data, get_admin_token, get_user_token
from rest_framework import status
from library import models
from library.tests.views.interface_test import ModelTestInterface


class MembersViewSetTest(ModelTestInterface, TestCase):
    multi_db = True
    @classmethod
    def setUpTestData(cls):
        users = get_test_data('users')
        for item in users:
            models.LibraryMember.objects.create_user(**item)
        models.LibraryMember.objects.create_superuser(
            username='admin', password='admin')

    @classmethod
    def tearDownClass(cls):
        models.LibraryMember.objects.all().delete()

# get list of users
    def test_get_object_list(self):
        """only admins are allowed to get the list of members"""
        access_token = get_admin_token(self)
        res = self.client.get(
            path=reverse('members-list'),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertIn('results', data)
        self.assertIn('count', data)
        user1 = data['results'][0]
        print(data)
        fields = ['username', 'first_name', 'last_name', 'email']
        self.assertListEqual(list(user1.keys()), fields)

    def test_get_object_list_normal_user(self):
        """Library members are not allowed to get list of members"""
        access_token = get_user_token(self)
        res = self.client.get(
            path=reverse('members-list'),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_object_list_unauthenticated_user(self):
        """Unauthorized user are not allowed to get list of members"""
        res = self.client.get(
            path=reverse('members-list'),
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# get user details
    def test_get_object_detail(self):
        """Only admins are allowed to get member details"""
        access_token = get_admin_token(self)
        res = self.client.get(
            path=reverse('members-detail', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        expected = {'username': 'user1', 'email': 'test@email.com',
                    'first_name': '', 'last_name': ''}
        self.assertEqual(data, expected)

    def test_get_non_existent_object(self):
        """Not found is returned for non-existent member id"""
        access_token = get_admin_token(self)
        res = self.client.get(
            path=reverse('members-detail', kwargs={'pk': -1}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_normal_user_get_object_detail(self):
        """Normal users are not allowed to get member details"""
        access_token = get_user_token(self)
        res = self.client.get(
            path=reverse('members-detail', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_get_object_detail(self):
        """Unauthenticated users are not allowed to get member details"""
        res = self.client.get(
            path=reverse('members-detail', kwargs={'pk': 1}),
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# get user profile
    def test_normal_user_get_profile(self):
        """Authenticated members can get their own profile data"""
        access_token = get_user_token(self)
        res = self.client.get(
            path=reverse('members-profile'),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        expected = {'username': 'user1', 'email': 'test@email.com',
                    'first_name': '', 'last_name': ''}
        self.assertEqual(data, expected)

    def test_unauthenticated_user_get_profile(self):
        """Unauthorized members cannot get profile data"""
        res = self.client.get(
            path=reverse('members-profile'),
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# update user profile
    def test_normal_user_update_profile(self):
        """Authenticated users can update their own profile"""
        access_token = get_user_token(self)
        data = {'email': 'changed_email@email.com'}
        res = self.client.patch(
            path=reverse('members-profile'),
            headers={'Authorization': f'Bearer {access_token}'},
            data=data,
            content_type='application/json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        expected = {"username": 'user1', 'email': 'changed_email@email.com',
                    'first_name': '', 'last_name': ''}
        self.assertEqual(data, expected)

# create user
    def test_admin_create_object(self):
        """Admin can create a library member"""
        data = {'username': 'user3', 'password': 'user3password'}
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('members-list'),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'},
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        actual = res.json()
        expected = {'username': 'user3', 'email': '',
                    'first_name': "", "last_name": ''}
        self.assertEqual(actual, expected)

    def test_create_object_with_existing_username(self):
        """Cannot create member with existing username"""
        data = {'username': 'user1', 'password': 'user3password'}
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('members-list'),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'},
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_missing_fields(self):
        """Cannot create a library member with incomplete fields"""
        data = {'username': 'user3'}
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('members-list'),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'},
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        data = {'password': 'user3password'}
        access_token = get_admin_token(self)
        res = self.client.post(
            path=reverse('members-list'),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'},
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_normal_user_create_object(self):
        """Members cannot create another member"""
        data = {'username': 'user3', 'password': 'user3password'}
        access_token = get_user_token(self)
        res = self.client.post(
            path=reverse('members-list'),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'},
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_create_object(self):
        """Unauthorized users cannot create a member."""
        data = {'username': 'user3', 'password': 'user3password'}
        res = self.client.post(
            path=reverse('members-list'),
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# update user
    def test_admin_update_object(self):
        """Admin cannot peform update"""
        access_token = get_admin_token(self)
        res = self.client.put(
            path=reverse('members-detail', kwargs={'pk': 1}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'},
            data={'username': 'UserNo12'}
        )
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_normal_user_update_object(self):
        """Authenticated user cannot update"""
        access_token = get_user_token(self)
        res = self.client.put(
            path=reverse('members-detail', kwargs={'pk': 1}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'},
            data={'username': 'UserNo12'}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_update_object(self):
        """Unauthenticated user cannot perform update"""
        res = self.client.put(
            path=reverse('members-detail', kwargs={'pk': 1}),
            content_type='application/json',
            data={'username': 'UserNo12'}
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# patch user
    def test_admin_patch_object(self):
        """Admin cannot patch user"""
        access_token = get_admin_token(self)
        res = self.client.patch(
            path=reverse('members-detail', kwargs={'pk': 1}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'},
            data={'username': 'UserNo12'}
        )
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_normal_user_patch_object(self):
        """Authenticated user cannot perform patch operation"""
        access_token = get_user_token(self)
        res = self.client.patch(
            path=reverse('members-detail', kwargs={'pk': 1}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'},
            data={'username': 'UserNo12'}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_patch_object(self):
        """Unauthenticated user cannot perform patch operation"""
        res = self.client.patch(
            path=reverse('members-detail', kwargs={'pk': 1}),
            content_type='application/json',
            data={'username': 'UserNo12'}
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# delete user
    def test_admin_delete_object(self):
        """Admin cannot perform delete"""
        access_token = get_admin_token(self)
        res = self.client.delete(
            path=reverse('members-detail', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_normal_user_delete_object(self):
        """Authenticated user cannot perform delete"""
        access_token = get_user_token(self)
        res = self.client.delete(
            path=reverse('members-detail', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'},
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_delete_object(self):
        """Unauthenticated user cannot perform delete"""
        res = self.client.delete(
            path=reverse('members-detail', kwargs={'pk': 1}),
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# change password
    def test_change_password(self):
        """Authenticated users can change their own password"""
        access_token = get_admin_token(self)
        data = {'new_password': 'newpasswordings', 'old_password': 'admin'}
        res = self.client.post(
            path=reverse('members-change-password'),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.post(
            content_type='application/json',
            data={"username": "admin", "password": "admin"},
            path=reverse('obtain_token')
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        res = self.client.post(
            content_type='application/json',
            data={"username": "admin", "password": "newpasswordings"},
            path=reverse('obtain_token')
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        access_token = get_user_token(self)
        data = {'new_password': 'newpasswordings', 'old_password': 'test'}
        res = self.client.post(
            path=reverse('members-change-password'),
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_unauthorized_user_change_password(self):
        """Unauthenticated users cannot change password"""
        data = {'new_password': 'newpasswordings', 'old_password': 'admin'}
        res = self.client.post(
            path=reverse('members-change-password'),
            content_type='application/json',
            data=data
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# deactivate account

    def test_admin_deactivate_account(self):
        """Admin have the authority to deactivate accounts"""
        access_token = get_admin_token(self)
        res = self.client.get(
            path=reverse('members-deactivate', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.post(
            content_type='application/json',
            data={"username": "user1", "password": "test"},
            path=reverse('obtain_token')
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        res = self.client.get(
            path=reverse('members-deactivate', kwargs={'pk': 2}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.post(
            content_type='application/json',
            data={"username": "admin", "password": "admin"},
            path=reverse('obtain_token')
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_deactivate_account(self):
        """Authenticated users can deactivate their accounts"""
        access_token = get_user_token(self)
        res = self.client.get(
            path=reverse('members-deactivate', kwargs={'pk': 2}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        res = self.client.get(
            path=reverse('members-deactivate', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.post(
            content_type='application/json',
            data={"username": "user1", "password": "test"},
            path=reverse('obtain_token')
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

# activate account
    def test_admin_activate_deactivated_account(self):
        """Admin can activate a deactivated account"""
        access_token = get_admin_token(self)

        # deactivate an account
        res = self.client.get(
            path=reverse('members-deactivate', kwargs={'pk': 1}),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.post(
            content_type='application/json',
            data={"username": "user1", "password": "test"},
            path=reverse('obtain_token')
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # username
        res = self.client.post(
            content_type='application/json',
            data={"username": "user1"},
            path=reverse('members-activate'),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.post(
            content_type='application/json',
            data={"username": "user1", "password": "test"},
            path=reverse('obtain_token')
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res = self.client.post(
            content_type='application/json',
            data={"username": "user3256"},
            path=reverse('members-activate'),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_activate_deactivated_account(self):
        """Users cannot activate their own accounts. Only admins are allowed."""
        access_token = get_user_token(self)
        res = self.client.post(
            content_type='application/json',
            data={"username": "user1"},
            path=reverse('members-activate'),
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
