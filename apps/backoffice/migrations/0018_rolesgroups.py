# Generated by Django 4.2.1 on 2024-08-02 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("backoffice", "0017_alter_user_password"),
    ]

    operations = [
        migrations.CreateModel(
            name="RolesGroups",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("usedBy", models.CharField(max_length=255)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="auth.group"
                    ),
                ),
            ],
            options={
                "db_table": "dyp_roles",
            },
        ),
    ]
