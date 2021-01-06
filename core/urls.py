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
    UserList,
    CategoryList,
    SaveProject,
    SavePlatform,
    SaveMarineGrowth,
    DeleteProject,
    DeletePlatform,
    UpdatePlatform,
    UpdateProject,
    DeleteMarineGrowth
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
    path("category/", CategoryList.as_view(), name="category-list"),
    path("saveproject/", SaveProject.as_view(), name="project-list"),
    path("saveplatform/", SavePlatform.as_view(), name="platform-list"),
    path("savemarinegrowth/", SaveMarineGrowth.as_view(), name="marine-list"),
    path("deletemarinegrowth/", DeleteMarineGrowth.as_view(), name="delete-marine-growth"),
    path("deleteproject/", DeleteProject.as_view(), name="project-delete"),
    path("deleteplatform/", DeletePlatform.as_view(), name="platform-delete"),
    path("updateproject/", UpdateProject.as_view(), name="project-update"),
    path("updateplatform/", UpdatePlatform.as_view(), name="platform-update"),
    path("", include(router.urls))
    # fmt: on
]
