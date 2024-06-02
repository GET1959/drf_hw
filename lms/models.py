from django.conf import settings
from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="lms/images", **NULLABLE, verbose_name="Просмотр", help_text="Загрузите изображение"
    )
    price = models.PositiveIntegerField(default=0, verbose_name="сумма оплаты")
    description = models.TextField(verbose_name="Описание", help_text="Добавьте описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец", help_text="Укажите владельца"
    )

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
    price = models.PositiveIntegerField(default=0, verbose_name="сумма оплаты")
    preview = models.ImageField(upload_to="lms/images", **NULLABLE, verbose_name="Просмотр",
                                help_text="Загрузите изображение")
    video = models.TextField(**NULLABLE, verbose_name="Ссылка на видео", help_text="Укажите ссылку на видео")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец", help_text="Укажите владельца"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
