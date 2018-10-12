from django.urls import path
from app.views import user_login_views as user_views
from app.views import app as app_views

urlpatterns = [
    # path(r'^', app_views.index, name='index'),

    path(r"login/", user_views.user_login, name='user_login'),
    path(r'register/', user_views.register, name='user_register'),
    path(r'logout/', user_views.user_logout, name='user_logout'),

    # path(r'models', views.models, name='models'),
]
