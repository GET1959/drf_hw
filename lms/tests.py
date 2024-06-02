from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import Subscription, User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(
            title="Знакомство с языком Python",
            description="Общие сведения о языке, установка начало работы.",
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Основы Python",
            description="Общие сведения о языке, установка начало работы.",
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("lms:lesson-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse("lms:lesson-create")
        data = {"title": "Python: переменные, списки, словари",
                "description": "Работа с переменными, списками, словарями", }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("lms:lesson-update", args=(self.lesson.pk,))
        data = {"title": "Python: переменные, списки, словари, кортежи"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Python: переменные, списки, словари, кортежи")

    def test_lesson_delete(self):
        url = reverse("lms:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "video": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(
            title="Знакомство с языком Python",
            description="Общие сведения о языке, установка начало работы.",
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        data = {"user": self.user.id, "course": self.course.id}
        url = reverse("users:subscription")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "подписка добавлена"})

    def test_unsubscribe(self):
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        data = {"user": self.user.id, "course": self.course.id}
        url = reverse("users:subscription")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "подписка удалена"})
