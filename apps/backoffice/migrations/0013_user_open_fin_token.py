# Generated by Django 4.2.1 on 2023-08-11 17:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backoffice", "0012_merge_20230726_1155"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="open_fin_token",
            field=models.TextField(null=True),
        ),
    ]
