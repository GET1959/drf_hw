from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView

app_name = LmsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
]
urlpatterns += router.urls