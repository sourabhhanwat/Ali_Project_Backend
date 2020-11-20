from django.conf import settings
from django.db import models
from django.db.models import Q


class ProjectQuerySet(models.QuerySet):
    def has_ownership(self, user: settings.AUTH_USER_MODEL):
        if user.is_superuser:
            return self

        return self.filter(
            Q(users=user) | Q(project_platform__users=user)
        ).distinct()


class Project(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500, default="", blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ProjectOwnership", related_name = 'projectownership')
    start_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    end_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProjectQuerySet.as_manager()

    def __str__(self):
        return self.name
