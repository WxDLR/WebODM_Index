from django.http import JsonResponse
from django.views import View
from guardian.shortcuts import get_perms
from rest_framework import serializers, viewsets, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from app import models
from app.models import Project
from app.models.user import MyUser
from .tasks import TaskIDsSerializer
from .MyUsers import MyUserSerializer

import django_filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskIDsSerializer(many=True, read_only=True)
    # owner = serializers.HiddenField(
    #         default=serializers.CurrentUserDefault()
    #     )
    owner = MyUserSerializer(read_only=True, )
    created_at = serializers.ReadOnlyField()
    # permissions = serializers.SerializerMethodField()

    # def get_permissions(self, obj):
    #     if 'request' in self.context:
    #         return list(map(lambda p: p.replace("_project", ""), get_perms(self.context['request'].user, obj)))
    #     else:
    #         # Cannot list permissions, no user is associated with request (happens when serializing ui test mocks)
    #         return []

    class Meta:
        model = models.Project
        exclude = ('deleting', )


class ProjectsPagination(PageNumberPagination):
    page_size = 5

    # Client can control the page using this query parameter.
    page_query_param = 'page'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = "pg"

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = 20
    last_page_strings = ('last',)


class ProjectFilter(FilterSet):
    high = django_filters.NumberFilter(name='id', lookup_expr='lte')
    low = django_filters.NumberFilter(name='id', lookup_expr='gte')

    class Meta:
        model = Project
        fields = ['high', 'low']


class ProjectPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            MyUser.objects.get(username=request.myuser)
            return True

        except MyUser.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.myuser


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Project get/add/delete/update
    Projects are the building blocks
    of processing. Each project can have zero or more tasks associated with it.
    Users can fine tune the permissions on projects, including whether users/groups have
    access to view, add, change or delete them.
    """
    serializer_class = ProjectSerializer
    queryset = models.Project.objects.prefetch_related('task_set').filter(deleting=False).order_by('-created_at')
    ordering_fields = '__all__'
    pagination_class = ProjectsPagination
    filter_backends = (DjangoFilterBackend, )
    filter_class = ProjectFilter
    permission_classes = (ProjectPermission,)











