"""
URL configuration for Actocode project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp.views import prant,home
from compiler.views import code_editor
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task.views import TaskViewSet,main_views,base,code_editor2,task_detail,profile_view,submission_list,dashboard,register_user,login_user,profile,logout_user,withdraw_coins,redeem_voucher,SubmissionViewSet,UserProfileViewSet
from task.views import (task_list)

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router = DefaultRouter()
router.register(r'submissions', SubmissionViewSet)
router.register(r'user-profile', UserProfileViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(router.urls)),
    path('prant',prant, name="prant"),
    path('',home, name="home"),
    path('',base, name="base"),
    path("editor", code_editor, name="editor"),
    path("editor2", code_editor2, name="editor2"),
    path("api/", include("compiler.urls")),
    path('task/', task_list,name="task"),
    path('dashboard/', dashboard, name="dashboard"),
    path('submissions/',submission_list, name='submission_list'),
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("profile/",profile, name="profile"),
    path("logout/", logout_user, name="logout"),
    path("withdraw/", withdraw_coins, name="withdraw"),
    path("redeem/", redeem_voucher, name="redeem"),
    path('<str:ref_code>/',main_views, name="main"),
    path("", main_views,name="raferlpage"),
    path("profile/", profile_view, name="profile"),
    path('task/<int:task_id>/', task_detail, name='task_detail'),

 
]

 
