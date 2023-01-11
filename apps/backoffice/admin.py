# Librerías de Terceros
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Proyecto
from .models import AuditModel, User


@admin.register(User)
class UserAdmin(UserAdmin):
    ordering = ["id"]
    list_display = ["id", "email", "password", "is_staff", "is_superuser"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        ("Personal Info", {"fields": ("username",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                )
            },
        ),
        ("Important Data", {"fields": ("last_login", "location")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(AuditModel)
class AuditModelAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = [
        "id",
        "table_modified",
        "columns_modified",
        "row_modified",
        "created_by",
        "request_method",
    ]
