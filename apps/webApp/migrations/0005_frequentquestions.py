# Generated by Django 4.2.1 on 2023-10-11 18:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("webApp", "0004_alter_customer_id_alter_paymentscustomer_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="FrequentQuestions",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("question", models.CharField(max_length=255)),
                ("answer", models.TextField()),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name_plural": "Frequent Questions",
            },
        ),
    ]
