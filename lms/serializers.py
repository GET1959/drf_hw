from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()  # 19.05.2024
    lesson_list = SerializerMethodField()

    def get_lesson_count(self, obj):  # 19.05.2024
        return Lesson.objects.filter(course=obj).count()  # 19.05.2024

    def get_lesson_list(self, obj):
        return [less.title for less in Lesson.objects.filter(course=obj)]

    class Meta:
        model = Course
        fields = ("title", "description", "lesson_count", "lesson_list")


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
