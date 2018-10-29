from django.apps import AppConfig

import xadmin
from xadmin import views

from app.models import PluginDatum, Project, Preset, Task, ImageUpload, Setting, Theme, user
from nodeodm.models import ProcessingNode

#
# class PluginDatumAdminx(object):
#     pass
#
#
# xadmin.site.register(PluginDatum, PluginDatumAdminx)


class ProjectAdminx(object):
    list_display = ('owner', 'name', 'description', 'created_at', 'deleting')


xadmin.site.register(Project, ProjectAdminx)


class MyUserAdminx(object):
    fields = ('username', 'password', 'email', 'phone_number')
    list_display = ('username', 'password', 'email', 'phone_number',)


xadmin.site.register(user.MyUser, MyUserAdminx)


class TaskAdminx(object):
    list_display = ('name', 'project', 'processing_time', 'status', 'created_at', 'public')


xadmin.site.register(Task, TaskAdminx)


class ImageUploadAdminx(object):
    list_display = ('task', 'image')


xadmin.site.register(ImageUpload, ImageUploadAdminx)


class ProcessingnodeAdminx(object):
    fields = ('hostname', 'port')
    list_display = ('hostname', 'port', 'api_version', 'queue_count', 'token')


xadmin.site.register(ProcessingNode, ProcessingnodeAdminx)


# Xadmin settings
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
    menu_style = "accordion"


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    site_title = 'WebODM后台管理系统'
    site_footer = '广州欧科信息技术股份有限公司'


xadmin.site.register(views.CommAdminView, GlobalSetting)


