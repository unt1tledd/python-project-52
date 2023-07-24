import os
import json
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy
from task_manager.tasks.models import Task
from django.utils.translation import gettext_lazy as _


class SetupTestTask(TestCase):
    fixtures = ['users.json', 'tasks.json', 'labels.json', 'statuses.json']

    def setUp(self):
        self.tasks = reverse_lazy('tasks')
        self.create = reverse_lazy('create_task')
        self.task = reverse_lazy('task', kwargs={"pk": 1})
        self.upd_task = reverse_lazy("update_task", kwargs={"pk": 1})
        self.del_task1 = reverse_lazy("delete_task", kwargs={"pk": 1})
        self.del_task2 = reverse_lazy("delete_task", kwargs={"pk": 2})
        self.user = get_user_model().objects.get(pk=1)
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        with open(os.path.join("fixtures", "test_task.json")) as f:
            self.test_task = json.load(f)


class TestTask(SetupTestTask):
    fixtures = ['users.json', 'tasks.json', 'labels.json', 'statuses.json']

    def test_tasks_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.tasks)
        self.assertEqual(response.status_code, 200)

    def test_task_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.task)
        self.assertEqual(response.status_code, 200)

    def test_create_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.create)
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        task_count = Task.objects.count()
        self.client.force_login(self.user)
        response = self.client.post(path=self.create, data=self.test_task)
        self.assertEqual(response.status_code, 302)
        self.task3 = Task.objects.get(pk=3)
        self.assertEqual(self.task3.name, self.test_task.get('name'))
        self.assertEqual(Task.objects.count(), task_count + 1)

    def test_upd_page(self):
        self.client.force_login(self.user)
        response = self.client.get(self.upd_task)
        self.assertEqual(response.status_code, 200)

    def test_upd_task(self):
        self.client.force_login(self.user)
        self.assertNotEqual(self.task1.name, self.test_task.get("name"))
        response = self.client.post(path=self.upd_task, data=self.test_task)
        self.assertEqual(response.status_code, 302)
        self.task = Task.objects.get(pk=1)
        self.assertEqual(self.task.name, self.test_task.get('name'))

    def test_delete_page(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.del_task1)
        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        task_count = Task.objects.count()
        self.client.force_login(self.user)
        response = self.client.delete(path=self.del_task1)
        self.assertEqual(first=response.status_code, second=302)
        task_count_after_delete = Task.objects.count()
        self.assertGreater(task_count, task_count_after_delete)
        with self.assertRaises(expected_exception=Task.DoesNotExist):
            Task.objects.get(pk=1)

    def test_delete_task_with_another_author(self):
        task_count = Task.objects.count()
        self.client.force_login(self.user)
        response = self.client.delete(path=self.del_task2)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response=response, expected_url=self.tasks)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(_('A task can only be deleted by its author.'), messages)
        self.assertEqual(Task.objects.all().count(), task_count)
