from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from lms.models import Course


@shared_task
def course_update_notification(course_id):
    """Уведомление пользователей об обновлении курса."""
    course = Course.objects.get(pk=course_id)
    # Подписки, ссылающиеся на курс.
    subs = course.subscription_set.all()
    subs = subs.select_related("user")

    recipient_list = subs.values_list("user__email", flat=True)
    send_mail(
        subject=f"Об изменениях в курсе {course.title}",
        message=f"Обновлен курс {course.title}. Изменения: {course.description}",
        recipient_list=recipient_list,
        from_email=settings.EMAIL_HOST_USER
    )
