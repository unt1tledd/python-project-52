import os
import json
from django.contrib.messages import get_messages
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class SetupTestStatus(TestCase):
    fixtures = ['status.json', 'users.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.statuses = reverse_lazy('statuses')
        self.create = reverse_lazy('create_status')
        self.upd_st1 = reverse_lazy('update_status', kwargs={'pk': 1})
        self.del_st1 = reverse_lazy('delete_status', kwargs={'pk': 1})
        self.del_st3 = reverse_lazy('delete_status', kwargs={'pk': 3})
        self.user = get_user_model().objects.get(pk=1)
        self.status1 = Status.objects.get(pk=1)
        with open(os.path.join('fixtures', 'test_status.json')) as f:
            self.test_status = json.load(f)


class TestStatus(SetupTestStatus):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_statuses_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.statuses)
        self.assertEqual(response.status_code, 200)

    def test_create_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.create)
        self.assertEqual(response.status_code, 200)

    def test_create_status(self):
        self.client.force_login(user=self.user)
        response = self.client.post(path=self.create, data=self.test_status)
        self.assertRedirects(response=response, expected_url=self.statuses)
        self.assertEqual(response.status_code, 302)
        self.status4 = Status.objects.get(pk=4)
        self.assertEqual(first=self.status4.name, second=self.test_status.get('name'))

    def test_update_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.upd_st1)
        self.assertEqual(response.status_code, 200)

    def test_upd_status(self):
        self.client.force_login(user=self.user)
        self.assertNotEqual(self.status1.name, self.test_status.get('name'))
        response = self.client.post(self.upd_st1, data=self.test_status)
        self.assertEqual(response.status_code, 302)
        self.status1 = Status.objects.get(pk=1)
        self.assertEqual(self.status1.name, self.test_status.get('name'))

    def test_delete_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.del_st1)
        self.assertEqual(response.status_code, 200)

    def test_delete_status(self):
        self.client.force_login(user=self.user)
        response = self.client.delete(path=self.del_st3)
        self.assertEqual(first=response.status_code, second=302)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=3)

    def test_delete_status_with_task(self):
        statuses_count = Status.objects.count()
        self.client.force_login(user=self.user)
        with self.assertRaises(expected_exception=ProtectedError):
            response = self.client.delete(path=self.del_st1)
            messages = [m.message for m in get_messages(response.wsgi_request)]
            self.assertIn(_('It`s not possible to delete the status that is being used'), messages)
        self.assertEqual(first=statuses_count, second=3)
