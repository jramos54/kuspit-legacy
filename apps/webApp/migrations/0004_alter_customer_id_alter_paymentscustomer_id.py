# Generated by Django 4.2.1 on 2023-07-26 17:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("webApp", "0003_auto_20230628_0839"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="paymentscustomer",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
