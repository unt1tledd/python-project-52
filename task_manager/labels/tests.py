import os
import json
from django.contrib.messages import get_messages
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class SetupTestLabel(TestCase):
    fixtures = ['status.json', 'users.json', 'labels.json', 'tasks.json']

    def setUp(self):
        self.labels = reverse_lazy('labels')
        self.create = reverse_lazy('create_label')
        self.upd_label = reverse_lazy('update_label', kwargs={'pk': 1})
        self.del_label1 = reverse_lazy('delete_label', kwargs={'pk': 1})
        self.del_label3 = reverse_lazy('delete_label', kwargs={'pk': 3})
        self.user = get_user_model().objects.get(pk=1)
        self.label = Label.objects.get(pk=1)
        with open(os.path.join('fixtures', 'test_label.json')) as f:
            self.test_label = json.load(f)


class TestLabel(SetupTestLabel):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']

    def test_labels_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.labels)
        self.assertEqual(response.status_code, 200)

    def test_create_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.create)
        self.assertEqual(response.status_code, 200)

    def test_create_label(self):
        self.client.force_login(user=self.user)
        response = self.client.post(path=self.create, data=self.test_label)
        self.assertRedirects(response=response, expected_url=self.labels)
        self.assertEqual(response.status_code, 302)
        self.label4 = Label.objects.get(pk=4)
        self.assertEqual(first=self.label4.name, second=self.test_label.get('name'))

    def test_update_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.upd_label)
        self.assertEqual(response.status_code, 200)

    def test_upd_label(self):
        self.client.force_login(user=self.user)
        self.assertNotEqual(self.label.name, self.test_label.get('name'))
        response = self.client.post(path=self.upd_label, data=self.test_label)
        self.assertEqual(response.status_code, 302)
        self.label = Label.objects.get(pk=1)
        self.assertEqual(self.label.name, self.test_label.get('name'))

    def test_delete_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.del_label1)
        self.assertEqual(response.status_code, 200)

    def test_delete_label(self):
        self.client.force_login(user=self.user)
        response = self.client.delete(path=self.del_label3)
        self.assertEqual(first=response.status_code, second=302)
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(pk=3)

    def test_delete_label_with_task(self):
        labels_count = Label.objects.count()
        self.client.force_login(user=self.user)
        with self.assertRaises(expected_exception=ProtectedError):
            response = self.client.delete(path=self.del_label1)
            messages = [m.message for m in get_messages(response.wsgi_request)]
            self.assertIn(_('It`s not possible to delete the label that is being used'), messages)
        self.assertEqual(first=labels_count, second=3)
