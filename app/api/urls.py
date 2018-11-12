from django.conf.urls import url, include
from django.urls import path

from app.api.presets import PresetViewSet
from app.api.users import MyUserViewSet
from app.plugins import get_api_url_patterns
from .projects import ProjectViewSet, MyProjectViewSet
from .tasks import TaskViewSet, TaskTiles, TaskTilesJson, TaskDownloads, TaskAssets, MyTaskViewSet
from .processingnodes import ProcessingNodeViewSet, ProcessingNodeOptionsView
from rest_framework_nested import routers
from rest_framework import routers as rf_routers
from rest_framework_jwt.views import obtain_jwt_token

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='projects')
router.register(r'processingnodes', ProcessingNodeViewSet)
router.register(r'presets', PresetViewSet, base_name='presets')
router.register(r'my_projects', MyProjectViewSet, base_name='my_projects')

tasks_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
tasks_router.register(r'tasks', TaskViewSet, base_name='projects-tasks')

rf_router = rf_routers.DefaultRouter()
rf_router.register(r'myusers', MyUserViewSet)
rf_router.register(r'mytasks', MyTaskViewSet)

urlpatterns = [
    url(r'processingnodes/options/$', ProcessingNodeOptionsView.as_view()),

    url(r'^', include(router.urls)),
    url(r'^', include(tasks_router.urls)),
    url(r'^', include(rf_router.urls)),

    url(r'^', include(tasks_router.urls)),

    url(
        r'projects/(?P<project_pk>[^/.]+)/tasks/(?P<pk>[^/.]+)/(?P<tile_type>orthophoto|dsm|dtm)/tiles/(?P<z>[\d]+)/(?P<x>[\d]+)/(?P<y>[\d]+)\.png$',
        TaskTiles.as_view()),
    url(r'projects/(?P<project_pk>[^/.]+)/tasks/(?P<pk>[^/.]+)/(?P<tile_type>orthophoto|dsm|dtm)/tiles\.json$',
        TaskTilesJson.as_view()),

    url(r'projects/(?P<project_pk>[^/.]+)/tasks/(?P<pk>[^/.]+)/download/(?P<asset>.+)$', TaskDownloads.as_view()),

    url(r'projects/(?P<project_pk>[^/.]+)/tasks/(?P<pk>[^/.]+)/assets/(?P<unsafe_asset_path>.+)$',
        TaskAssets.as_view()),

    url(r'^auth/', include('rest_framework.urls')),

    url(r'^token-auth/', obtain_jwt_token),
]

urlpatterns += get_api_url_patterns()
