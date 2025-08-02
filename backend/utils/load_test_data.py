import json
import os
from library import models
from django.urls import reverse


def get_test_data(key):
    file_path = os.getcwd() + "/utils/test_data.json"
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    if key:
        return data[key]
    return data


def get_admin_token(test, refresh=False):
    res_payload = test.client.post(
        reverse('obtain_token'),
        content_type='application/json',
        data={'username': 'admin', 'password': 'admin'}
    ).json()
    jwt_token = res_payload['access']
    refresh_token = res_payload['refresh']
    if refresh:
        return jwt_token, refresh_token
    else:
        return jwt_token


def get_user_token(test, refresh=False):
    res_payload = test.client.post(
        reverse('obtain_token'),
        content_type='application/json',
        data={'username': 'user1', 'password': 'test'}
    ).json()
    jwt_token = res_payload['access']
    refresh_token = res_payload['refresh']
    if refresh:
        return jwt_token, refresh_token
    else:
        return jwt_token
