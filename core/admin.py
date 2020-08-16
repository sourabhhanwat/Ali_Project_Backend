import logging

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import (
    Project,
    User,
    Site,
    ProjectOwnership,
    Platform,
    SiteOwnership,
    PlatformOwnership,
)

logger = logging.getLogger("core.admin")


class ProjectOwnershipInline(admin.TabularInline):
    model = ProjectOwnership
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (ProjectOwnershipInline,)


class SiteOwnershipInline(admin.TabularInline):
    model = SiteOwnership
    extra = 1


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name", "project_name")
    inlines = (SiteOwnershipInline,)

    def project_name(self, obj):
        return obj.project.name


class PlatformOwnershipInline(admin.TabularInline):
    model = PlatformOwnership
    extra = 1


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("name", "project_name", "site_name")
    fieldsets = (("General Details", {"fields": ("name", "site", "description")},),)
    inlines = (PlatformOwnershipInline,)

    def project_name(self, obj):
        return obj.site.project.name

    def site_name(self, obj):
        return obj.site.name


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser"),}),
    )
    inlines = (ProjectOwnershipInline, SiteOwnershipInline, PlatformOwnershipInline)


admin.site.unregister(Group)

admin.site.site_header = "RBUI Administration"
admin.site.site_title = "RBUI Administration"
