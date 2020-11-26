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
    PlatformMannedStatus,
    EconomicImpactConsequence,
    EnvironmentalConsequence,
)

logger = logging.getLogger("core.admin")


class ProjectOwnershipInline(admin.TabularInline):
    model = ProjectOwnership
    extra = 1


# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     inlines = (ProjectOwnershipInline,)


class SiteOwnershipInline(admin.TabularInline):
    model = SiteOwnership
    extra = 1


# @admin.register(Site)
# class SiteAdmin(admin.ModelAdmin):
#     list_display = ("name", "project_name")
#     inlines = (SiteOwnershipInline,)

#     def project_name(self, obj):
#         return obj.project.name


class PlatformOwnershipInline(admin.TabularInline):
    model = PlatformOwnership
    extra = 1


# @admin.register(Platform)
# class PlatformAdmin(admin.ModelAdmin):
#     list_display = ("name", "project_name", "environmental_consequence_category", "economic_consequence_category")
#     fieldsets = (("General Details", {"fields": ("name","project", "description","environmental_consequence_category","economic_consequence_category","level_1_last_inspection_date","level_2_last_inspection_date","level_3_last_inspection_date","level_1_selected_inspection_interval_for_next_inspection","level_2_selected_inspection_interval_for_next_inspection","level_3_selected_inspection_interval_for_next_inspection")},),)
#     inlines = (PlatformOwnershipInline,)

#     def project_name(self, obj):
#         return obj.project.name


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser","project_create_access"),}),
    )
    inlines = (ProjectOwnershipInline, PlatformOwnershipInline)

# @admin.register(PlatformMannedStatus)
# class PlatformMannedStatusAdmin(admin.ModelAdmin):
#     list_display=('name','ranking','description')

# @admin.register(EconomicImpactConsequence)
# class EconomicImpactConsequenceAdmin(admin.ModelAdmin):
#     list_disply='__all__'

# @admin.register(EnvironmentalConsequence)
# class EnvironmentalConsequenceAdmin(admin.ModelAdmin):
#     list_diplay="__all__"

admin.site.unregister(Group)

admin.site.site_header = "RBUI Administration"
admin.site.site_title = "RBUI Administration"
