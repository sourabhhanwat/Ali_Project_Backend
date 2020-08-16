import logging

from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets, mixins, filters, exceptions
from rest_framework.response import Response

from .models import (
    User,
    Project,
    Site,
    Platform,
    PlatformType,
    BracingType,
    NumberOfLegsType,
    PlatformMannedStatus,
    MarineGrowth,
)
from .serializers import (
    UserSerializer,
    ProjectSerializer,
    SiteSerializer,
    PlatformSerializer,
    PlatformTypeSerializer,
    BracingTypeSerializer,
    NumberOfLegsTypeSerializer,
    PlatformMannedStatusSerializer,
    MarineGrowthSerializer,
)

logger = logging.getLogger("core.views")


class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Get user by id

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.kwargs.update({self.lookup_field: self.request.user.id})
        return super().retrieve(request, *args, **kwargs)


class OwnedResourceFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.has_ownership(request.user)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filter_backends = [OwnedResourceFilter, DjangoFilterBackend]


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SiteSerializer
    queryset = Site.objects.all()
    filter_backends = [OwnedResourceFilter, DjangoFilterBackend]
    filterset_fields = ["project"]


class PlatformFilter(FilterSet):
    class Meta:
        model = Platform
        fields = ["site", "site__project"]


class PlatformViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = PlatformSerializer
    queryset = Platform.objects.all()
    filter_backends = [OwnedResourceFilter, DjangoFilterBackend]
    filterset_class = PlatformFilter

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance: Platform = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if not request.user.is_superuser:
            platform = Platform.objects.filter(pk=instance.id).with_access_type(
                user=request.user
            )[0]
            if platform.access_type != "M":
                raise exceptions.PermissionDenied()

        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class PlatformTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlatformTypeSerializer
    queryset = PlatformType.objects.all()


class BracingTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BracingTypeSerializer
    queryset = BracingType.objects.all()


class NumberOfLegsTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NumberOfLegsTypeSerializer
    queryset = NumberOfLegsType.objects.all()


class PlatformMannedStatusViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PlatformMannedStatusSerializer
    queryset = PlatformMannedStatus.objects.all()


class MarineGrowthFilter(FilterSet):
    class Meta:
        model = MarineGrowth
        fields = ["platform"]


class MarineGrowthViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, OwnedResourceFilter]
    serializer_class = MarineGrowthSerializer
    queryset = MarineGrowth.objects.all()
    filterset_class = MarineGrowthFilter
