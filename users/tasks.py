from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from users.models import User


@shared_task
def auto_block_user():
    month_ago = timezone.now() + relativedelta(months=-1)
    users_for_block = User.objects.filter(is_active=True, last_login__lte=month_ago)

    users_for_block.update(is_active=False)
