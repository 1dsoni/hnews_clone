"""hnews_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
import django.contrib.auth.urls
from dashboard import views as dashboard_views
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView

from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', dashboard_views.signup, name='signup'),
    path('delete/<int:article_id>', dashboard_views.delete_article, name='delete'),
    path('undelete/<int:article_id>', dashboard_views.undelete_article, name='undelete'),
    path('read/<int:article_id>', dashboard_views.read_article, name='read'),
    path('deleted_articles/', dashboard_views.deleted_articles_view, name='deleted_articles'),
    path('', dashboard_views.index_view, name='home' ),
]
