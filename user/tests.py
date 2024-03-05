from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.models import User, Log
from user.serializers import UserSerializer, LogSerializer


# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {"name": "test", "email": "test@gmail.com", "password": "test"}
        self.response = self.client.post(
            reverse("user-list"), self.user_data, format="json"
        )

    def test_api_can_create_a_user(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_user(self):
        user = User.objects.get()
        response = self.client.get(
            reverse("user-detail", kwargs={"pk": user.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, user)

    def test_api_can_update_user(self):
        user = User.objects.get()
        change_user = {"name": "test", "email": "test@gmail.com", "password": "testupdated"}
        response = self.client.put(
            reverse("user-detail", kwargs={"pk": user.id}), change_user, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_user(self):
        user = User.objects.get()
        response = self.client.delete(
            reverse("user-detail", kwargs={"pk": user.id}), format="json", follow=True
        )
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_can_get_all_users(self):
        response = self.client.get(reverse("user-list"), format="json")
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name="test", email="test@gmail.com", password="test")
        self.log_data = {"user": self.user.id, "action": "check_in", "status": "in_progress"}
        self.response = self.client.post(
            reverse("log-list"), self.log_data, format="json"
        )

    def test_api_can_create_a_log(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_log(self):
        log = Log.objects.get()
        response = self.client.get(
            reverse("log-detail", kwargs={"pk": log.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], log.id)

    def test_api_can_update_log(self):
        log = Log.objects.get()
        change_log = {"user": self.user.id, "action": "check_in", "status": "completed"}
        response = self.client.put(
            reverse("log-detail", kwargs={"pk": log.id}), change_log, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_delete_log(self):
        log = Log.objects.get()
        response = self.client.delete(
            reverse("log-detail", kwargs={"pk": log.id}), format="json", follow=True
        )
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_can_get_all_logs(self):
        response = self.client.get(reverse("log-list"), format="json")
        logs = Log.objects.all()
        serializer = LogSerializer(logs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_get_logs_by_user(self):
        response = self.client.get(reverse("log-list"), format="json")
        logs = Log.objects.filter(user=self.user.id)
        serializer = LogSerializer(logs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_get_logs_by_action(self):
        response = self.client.get(reverse("log-list"), format="json")
        logs = Log.objects.filter(action="check_in")
        serializer = LogSerializer(logs, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)