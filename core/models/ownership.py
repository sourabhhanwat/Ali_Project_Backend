from django.conf import settings
from django.db import models


class PlatformOwnership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    platform = models.ForeignKey("Platform", on_delete=models.CASCADE)
    assign_time = models.DateTimeField(auto_now=True)

    AccessType = [
        ('V', 'View'),
        ('M', 'Modify'),
    ]

    access_type = models.CharField(
        max_length=1, choices=AccessType, default='V'
    )

    def __str__(self):
        return f"User {self.user.username} manage Platform {self.platform.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "platform"], name="unique_platform_ownership"
            )
        ]


class ProjectOwnership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "core_user")
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name="project_name")
    assign_time = models.DateTimeField(auto_now=True)

    AccessType = [
        ('V', 'View'),
        ('M', 'Modify'),
    ]

    access_type = models.CharField(
        max_length=1, choices=AccessType, default='V'
    )

    def __str__(self):
        return f"User {self.user.username} manage Project {self.project.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "project"], name="unique_project_ownership"
            )
        ]


class SiteOwnership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    site = models.ForeignKey("Site", on_delete=models.CASCADE)
    assign_time = models.DateTimeField(auto_now=True)

    AccessType = [
        ('V', 'View'),
        ('M', 'Modify'),
    ]

    access_type = models.CharField(
        max_length=1, choices=AccessType, default='V'
    )

    def __str__(self):
        return f"User {self.user.username} manage Site {self.site.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "site"], name="unique_site_ownership"
            )
        ]
