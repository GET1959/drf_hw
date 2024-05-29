from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson
from lms.validators import VideoValidator
from users.models import Subscription


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField(read_only=True)
    lesson_list = SerializerMethodField(read_only=True)
    is_subscribed = SerializerMethodField(read_only=True)

    def get_lesson_count(self, obj):  # 19.05.2024
        return Lesson.objects.filter(course=obj).count()

    def get_lesson_list(self, obj):
        return [less.title for less in Lesson.objects.filter(course=obj)]

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if Subscription.objects.filter(user=user, course=obj).exists():
            return True
        return False

    class Meta:
        model = Course
        fields = ("id", "title", "description", "lesson_count", "lesson_list", "is_subscribed", "owner")


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoValidator(field="video")]
