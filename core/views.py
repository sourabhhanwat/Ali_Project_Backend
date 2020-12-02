import logging
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets, mixins, filters, exceptions
from rest_framework.response import Response
from django.http import JsonResponse

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
    ProjectOwnership,
    SiteOwnership,
    PlatformOwnership
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
    ProjectOwnershipSerializer,
    SiteOwnershipSerializer,
    PlatformOwnershipSerializer
)

logger = logging.getLogger("core.views")

class UserList(APIView):
    def get(self,request):
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)

class SaveProject(APIView):
    def get(self,request):
        projects = Project.objects.all()
        p_serializers = ProjectSerializer(projects, many=True).data
        return Response(p_serializers)
    def post(self,request):
        try:
            data=request.data
            user = request.user

            if user.project_create_access == True or user.is_superuser==True:
                name = data.get('Name')
                user_id = data.get('Responsible')
                description = data.get('Description')
                startdate = data.get('StartDate')
                enddate = data.get('EndDate')
                project = Project(
                    name=name,
                    description=description,
                    start_date=startdate,
                    end_date=enddate,
                )
                project.save()
                projectowner = ProjectOwnership(
                    project=project,
                    user_id=user_id,
                    view_access=True,
                    platform_create_access=True,
                    delete_access=True,
                )
                projectowner.save()
                print(name)
                return Response({"status":True})
                
            return Response({"status":False})
        except:
            return Response({'status':False})
        
class SavePlatform(APIView):
    def get(self,request):
        return Response('Save Platform')
    def post(self, request):
        try:
            user = request.user
            print("User ",user)

            data = request.data
            print(data)
            name = data.get('Name')
            description = data.get('Description')
            startdate = data.get('StartDate')
            user_id = data.get('Responsible')
            project_id = data.get('Project')
            if user.is_superuser==True:
                platform = Platform(
                    name = name, 
                    description = description,
                    project_id = project_id
                )
                platform.save()

                platformowner = PlatformOwnership(
                    platform = platform,
                    user_id = user_id,
                    view_access=True,
                )
                platformowner.save()
                return Response({"status":True})
                            
            user_ownership = ProjectOwnership.objects.filter(user=user, project_id=project_id).first()
            if user_ownership:
                if user_ownership.platform_create_access == True:

                    platform = Platform(
                        name = name, 
                        description = description,
                        project_id = project_id
                    )
                    platform.save()

                    platformowner = PlatformOwnership(
                        platform = platform,
                        user_id = user_id,
                    )
                    platformowner.save()
                    return Response({"status":True})
            return Response({"status":False})

        except:
            return Response({'status':False})

class SaveMarineGrowth(APIView):
    def get(self,request):
        return Response("save Marine growth")
    def post(self,request):
        try:
            user = request.user
            data = request.data
            platform_id = data.get('platform_id')
            if user.is_superuser==True:
                mg_depths_from_el = data.get('marine_growth_depths_from_el')
                mg_depths_to_el = data.get('marine_growth_depths_to_el')
                mg_design_thickness = data.get('marine_growth_design_thickness')
                mg_inspected_thickness = data.get('marine_growth_inspected_thickness')
                platform_id = data.get('platform_id')
                mg = MarineGrowth(
                    marine_growth_depths_from_el = mg_depths_from_el,
                    marine_growth_depths_to_el = mg_depths_to_el,
                    marine_growth_inspected_thickness = mg_inspected_thickness,
                    marine_growth_design_thickness = mg_design_thickness,
                    platform_id = platform_id
                )
                mg.save()

                return Response({"status":True})

            user_ownership = PlatformOwnership.objects.filter(user=user, platform_id = platform_id).first()
            if user_ownership:
                if user_ownership.modify_access == True:
                    mg_depths_from_el = data.get('marine_growth_depths_from_el')
                    mg_depths_to_el = data.get('marine_growth_depths_to_el')
                    mg_design_thickness = data.get('marine_growth_design_thickness')
                    mg_inspected_thickness = data.get('marine_growth_inspected_thickness')
                    platform_id = data.get('platform_id')
                    mg = MarineGrowth(
                        marine_growth_depths_from_el = mg_depths_from_el,
                        marine_growth_depths_to_el = mg_depths_to_el,
                        marine_growth_inspected_thickness = mg_inspected_thickness,
                        marine_growth_design_thickness = mg_design_thickness,
                        platform_id = platform_id
                    )
                    mg.save()

                    print(data)
                    return Response({"status":True})
            return Response({"status":False})
        except:
            return Response({"status":False})

class DeletePlatform(APIView):
    def get(self,request):
        return Response("Delete platform")
    def post(self,request):
        try:
            user = request.user
            data = request.data
            platform_id = data.get('platformId')
            if user.is_superuser==True:
                platform = Platform.objects.get(id = platform_id).delete()

                return Response({"status":True})   

            user_ownership = PlatformOwnership.objects.filter(user=user, platform_id = platform_id).first()
            if user_ownership:
                if user_ownership.delete_access==True:
                    platform = Platform.objects.get(id = platform_id).delete()

                    return Response({"status":True})
            return Response({"status":False})
        except:
            return Response({"status":False})

class DeleteProject(APIView):
    def get(self,request):
        return Response("Delete project")
    def post(self,request):
        try:
            user = request.user
            data = request.data
            project_id = data.get('projectId')
            if user.is_superuser==True:
                project = Project.objects.get(id = project_id).delete()

                return Response({"status":True})          
            
            user_ownership = ProjectOwnership.objects.filter(user=user, project_id=project_id).first()
            if user_ownership:
                if user_ownership.delete_access==True:
                    project = Project.objects.get(id = project_id).delete()

                    return Response({"status":True})

            return Response({"status":False})
        except:
            return Response({"status":False})

class UpdateProject(APIView):
    def get(self,request):
        return Response("Update project")
    def post(self,request):
        try:
            user=request.user
            data = request.data
            name = data.get('Name')
            user_id = data.get('Responsible')
            description = data.get('Description')
            startdate = data.get('StartDate')
            enddate = data.get('EndDate')
            project_id = data.get('projectId')
            if user.is_superuser==True:
                project = Project.objects.filter(id = project_id).first()
                project.name = name
                project.description = description
                project.startdate = startdate
                project.enddate = enddate

                project_owned = ProjectOwnership.objects.filter(project_id = project_id).first()
                project_owned.user_id = user_id

                project_owned.save()

                project.save()

                return Response({"status":True})
            
            user_ownership = ProjectOwnership.objects.filter(user=user, project_id=project_id).first()
            if user_ownership:
                if user_ownership.modify_access==True:
                    project = Project.objects.filter(id = project_id).first()
                    project.name = name
                    project.description = description
                    project.startdate = startdate
                    project.enddate = enddate

                    project_owned = ProjectOwnership.objects.filter(project_id = project_id).first()
                    project_owned.user_id = user_id

                    project_owned.save()

                    project.save()


                    return Response({"status":True})
            return Response({"status":False})
        except:
            return Response({"status":False})

class UpdatePlatform(APIView):
    def get(self,request):
        return Response("Update platform")
    def post(self,request):
        try:
            user=request.user
            data = request.data
            name = data.get('Name')
            description = data.get('Description')
            startdate = data.get('StartDate')
            user_id = data.get('Responsible')
            project_id = data.get('Project')
            platform_id = data.get('platformId')

            if user.is_superuser==True:
                platform = Platform.objects.filter(id = platform_id).first()
                platform.name = name
                platform.description = description
                platform.project_id = project_id
                
                platform_owned = PlatformOwnership.objects.filter(platform_id = platform_id).first()
                platform_owned.user_id = user_id

                platform_owned.save()
                platform.save()

                return Response({"status":True})

            user_ownership = PlatformOwnership.objects.filter(user=user, platform_id = platform_id).first()
            if user_ownership:
                if user_ownership.modify_access == True:

                    platform = Platform.objects.filter(id = platform_id).first()
                    platform.name = name
                    platform.description = description
                    platform.project_id = project_id
                    
                    platform_owned = PlatformOwnership.objects.filter(platform_id = platform_id).first()
                    platform_owned.user_id = user_id

                    platform_owned.save()
                    platform.save()

                    return Response({"status":True})
            return Response({"status":False})
        except:
            return Response({"status":False})

class CategoryList(APIView):
    def get(self,request):
        categories = ['A','B','C','D','E']
        return Response(categories)


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
        fields = ["name", "project__name"]

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
        # print("\n*********** ",request.data)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # if not request.user.is_superuser:
        #     platform = Platform.objects.filter(pk=instance.id).with_access_type(
        #         user=request.user
        #     )[0]
        #     if platform.access_type != "M":
        #         raise exceptions.PermissionDenied()
        # print("user 1 ",request.user)
        if not request.user.is_superuser:
            print('aman')
            platform = PlatformOwnership.objects.filter(pk=instance.id, user=request.user).first()
            if platform.modify_access != True:
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
