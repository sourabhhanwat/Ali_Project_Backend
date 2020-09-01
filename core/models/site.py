from django.conf import settings
from django.db import models
from django.db.models import Q

from .project import Project


class SiteQuerySet(models.QuerySet):
    def has_ownership(self, user: settings.AUTH_USER_MODEL):
        if user.is_superuser:
            return self

        return self.filter(
            Q(users=user) | Q(project__users=user) | Q(platform__users=user)
        ).distinct()


class Site(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500, default="", blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_site')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="SiteOwnership")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SiteQuerySet.as_manager()

    def __str__(self):
        return self.name
