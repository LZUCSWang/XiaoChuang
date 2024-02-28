"""OCSIP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from home.views import (
    show_explore,
    show_diary,
    show_station,
    submit_survey,
    show_article,
    show_survey,
    show_music,
    home,
    django_upload_data,
    django_login,
    usr,
    django_create_dataset,
    django_delete_data,
    django_rename_dataset,
    django_delete_dataset,
    django_research_dataset,
    show_Hitokoto
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("usr/<str:token>", usr, name="usr"),
    path("home/", home, name="home"),
    path("", show_Hitokoto, name="Hitokoto"),
    path("login", django_login, name="login"),
    path("upload_data/", django_upload_data, name="add"),
    path("create_dataset/", django_create_dataset, name="create_dataset"),
    path("delete_data/", django_delete_data, name="delete_data"),
    path("rename_dataset/", django_rename_dataset, name="rename_dataset"),
    path("delete_dataset/", django_delete_dataset, name="delete_dataset"),
    path("research_dataset/", django_research_dataset, name="research_dataset"),
    path("show_article/", show_article, name="show_article"),
    path("show_survey/", show_survey, name="show_survey"),
    path("show_music/", show_music, name="show_music"),
    path("submit_survey/", submit_survey, name="submit_survey"),
    path("show_station/", show_station, name="show_station"),
    path("show_diary/", show_diary, name="show_diary"),
    path("show_explore/", show_explore, name="show_explore"),
    # path("Hitokoto/",show_Hitokoto,name="Hitokoto")
]
