from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    ProjectViewSet,
    SiteViewSet,
    PlatformViewSet,
    PlatformTypeViewSet,
    BracingTypeViewSet,
    NumberOfLegsTypeViewSet,
    PlatformMannedStatusViewSet,
    MarineGrowthViewSet,
    UserList
)

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"sites", SiteViewSet, basename="site")
router.register(r"platforms", PlatformViewSet, basename="platform")
router.register(r"platform-types", PlatformTypeViewSet, basename="platform-type")
router.register(r"bracing-types", BracingTypeViewSet, basename="bracing-type")
router.register(r"number-of-legs-types", NumberOfLegsTypeViewSet, basename="number-of-legs-types")
router.register(r"platform-manned-statuses",PlatformMannedStatusViewSet,basename="platform-manned-statuses",)
router.register(r"marine-growths", MarineGrowthViewSet, basename="marine-growths")

urlpatterns = [
    # fmt: off
    path("users/me/", UserViewSet.as_view({"get": "retrieve"}), name="user-detail"),
    path("users/", UserList.as_view(), name="user-list"),
    path("", include(router.urls))
    # fmt: on
]
