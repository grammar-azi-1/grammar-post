from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from ..models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "is_staff", "is_active", "profile_picture_preview")
    list_filter = ("email", "is_staff", "is_active",)
    readonly_fields = ("profile_picture_preview",)

    fieldsets = (
        (None, {
            "fields": (
                "email", "password", "username", "profile_picture", "profile_picture_preview", "bio", "slug"
            )
        }),
        ("Permissions", {
            "fields": ("is_staff", "is_active", "groups", "user_permissions")
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "username", "password1", "password2", "profile_picture", "bio",
                "is_staff", "is_active", "groups", "user_permissions"
            ),
        }),
    )

    search_fields = ("email", "username")
    ordering = ("email",)

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.profile_picture.url)
        return "No Image"

    profile_picture_preview.short_description = "Profile Preview"



admin.site.register(CustomUser, CustomUserAdmin)