from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as CustomUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from core.apps.accounts.models.user import User

admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(CustomUserAdmin):
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", 'role')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "usable_password", "password1", "password2"),
            },
        ),
    )
    list_display = ("phone", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("phone", "first_name", "last_name", "email")
    ordering = ("phone",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
