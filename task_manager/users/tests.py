import os
import json
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from task_manager.users.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class TestUser(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        self.create = reverse_lazy('create')
        self.users = reverse_lazy('users')
        self.login = reverse_lazy('login')
        self.user1 = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=2)
        self.upd_user1 = reverse_lazy('update', kwargs={'pk': 1})
        self.del_user1 = reverse_lazy('delete', kwargs={'pk': 1})
        self.upd_user2 = reverse_lazy('update', kwargs={'pk': 2})
        self.del_user2 = reverse_lazy('delete', kwargs={'pk': 2})
        with open(os.path.join('fixtures', 'test_user.json')) as f:
            self.test_user = json.load(f)

    def test_create(self):
        response = self.client.get(self.create)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.client.post(path=self.create, data=self.test_user)
        self.assertRedirects(response, self.login, 302)
        self.user = get_user_model().objects.get(pk=3)
        self.assertEqual(first=self.user.username, second=self.test_user.get('username'))
        self.assertEqual(first=self.user.first_name, second=self.test_user.get('first_name'))
        self.assertEqual(first=self.user.last_name, second=self.test_user.get('last_name'))

    def test_user_form_with_data(self):
        user_form = CustomUserCreationForm(data=self.test_user)
        self.assertTrue(user_form.is_valid())
        self.assertEqual(len(user_form.errors), 0)

    def test_user_form(self):
        user_form = CustomUserCreationForm(data={})
        self.assertFalse(user_form.is_valid())
        self.assertEqual(len(user_form.errors), 3)

    def test_upd_page(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.upd_user1)
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        self.client.force_login(self.user1)
        self.assertNotEqual(self.user1.username, self.test_user.get('username'))
        response = self.client.post(self.upd_user1, data=self.test_user)
        self.assertEqual(response.status_code, 302)
        self.user1 = get_user_model().objects.get(pk=1)
        self.assertEqual(self.user1.username, self.test_user.get('username'))

    def test_update_other_user(self):
        self.client.force_login(self.user2)
        response = self.client.post(self.upd_user1, data=self.test_user)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(_("You don't have permissions to update and delete another user"), messages)
        self.assertRedirects(response, self.users, 302, 200)

    def test_open_delete_page(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.del_user1)
        self.assertEqual(response.status_code, 200)
        self.client.force_login(self.user2)
        response = self.client.get(self.del_user1)
        self.assertEqual(response.status_code, 302)

    def test_delete_user(self):
        self.client.force_login(self.user2)
        response = self.client.delete(self.del_user2)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 1)
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(pk=2)

    def test_delete_other_user(self):
        users_count = get_user_model().objects.count()
        self.client.force_login(self.user2)
        response = self.client.post(self.del_user1)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(_("You don't have permissions to update and delete another user"), messages)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), users_count)
