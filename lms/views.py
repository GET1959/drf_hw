from datetime import datetime, timedelta

import pytz
from django.conf import settings
from rest_framework import viewsets
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from lms.models import Course, Lesson
from lms.paginators import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer
from lms.tasks import course_update_notification
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if not self.request.user.groups.filter(name='moderator').exists():
            return Course.objects.filter(owner=self.request.user)
        return Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModerator,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModerator | IsOwner,)
        return super().get_permissions()

    def perform_update(self, serializer):
        """При внесении изменений в курс отправляет уведомление подписанным польователям."""
        up_course = serializer.save()
        # timezone = pytz.timezone(settings.TIME_ZONE)
        # now = datetime.now(timezone)
        # four_days = timedelta(days=4)
        # has_passed = now - up_course.up_date
        # if has_passed > four_days:
        #     course_update_notification.delay(up_course.id)
        # up_course.up_date = now
        course_update_notification.delay(up_course.id)
        up_course.save()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if not self.request.user.groups.filter(name='moderator').exists():
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.all()


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner | IsModerator,)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner | IsModerator,)

    def perform_update(self, serializer):
        """При внесении изменений в урок отправляет уведомление подписанным польователям."""
        up_lesson = serializer.save()
        timezone = pytz.timezone(settings.TIME_ZONE)
        now = datetime.now(timezone)
        four_days = timedelta(days=4)
        has_passed = now - up_lesson.up_date
        if has_passed > four_days:
            course_update_notification.delay(up_lesson.course_id)
        up_lesson.up_date = now
        up_lesson.save()


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner,)
