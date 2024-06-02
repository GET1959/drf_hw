from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Укажите почту")
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name="Телефон", help_text="Укажите телефон")
    city = models.CharField(max_length=50, **NULLABLE, verbose_name="Город", help_text="Укажите город")
    avatar = models.ImageField(
        upload_to="users/avatars", **NULLABLE, verbose_name="Аватар", help_text="Загрузите аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    P_METHOD_CHOICES = [("cash", "cash"), ("transfer", "transfer")]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    payment_date = models.DateField(auto_now_add=True, verbose_name="дата платежа")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name="оплаченный курс")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name="оплаченный урок")
    amount = models.IntegerField(verbose_name="сумма оплаты")
    payment_method = models.CharField(max_length=150, choices=P_METHOD_CHOICES, verbose_name="способ платежа")

    def __str__(self):
        return f"Оплата от {self.payment_date}, {self.amount}"

    class Meta:
        verbose_name = "оплата"
        verbose_name_plural = "оплата"


class SendPayment(models.Model):
    payment_date = models.DateField(auto_now_add=True, verbose_name="дата платежа")
    session_id = models.CharField(max_length=255, **NULLABLE, verbose_name="Id сессии", help_text="Введите Id сессии")
    link = models.URLField(max_length=400, **NULLABLE, verbose_name="Ссылка на оплату", help_text="Укажите ссылку")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name="оплачиваемый курс")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name="оплачиваемый урок")
    payer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="плательщик")

    def __str__(self):
        return f"Оплата от {self.payment_date}, {self.payer}"

    class Meta:
        verbose_name = "оплата услуг"
        verbose_name_plural = "оплата услуг"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="курс")
    update_date = models.DateField(auto_now_add=True, verbose_name="дата обновления")
