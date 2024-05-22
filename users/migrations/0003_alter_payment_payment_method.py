# Generated by Django 5.0.6 on 2024-05-21 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="payment_method",
            field=models.CharField(
                choices=[("cash", "cash"), ("transfer", "transfer")], max_length=150, verbose_name="способ платежа"
            ),
        ),
    ]
