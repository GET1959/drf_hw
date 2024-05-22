from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="lms/images", **NULLABLE, verbose_name="Просмотр", help_text="Загрузите изображение"
    )
    description = models.TextField(verbose_name="Описание", help_text="Добавьте описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", help_text="Добавьте описание")
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="Курс", help_text="Укажите курс", **NULLABLE
    )
    preview = models.ImageField(upload_to="lms/images", **NULLABLE, verbose_name="Просмотр",
                                help_text="Загрузите изображение")
    video = models.TextField(**NULLABLE, verbose_name="Ссылка на видео", help_text="Укажите ссылку на видео")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
