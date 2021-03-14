"""capstone_HomeIOT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from homeiotapi.views import register_user, login_user, UsersViewSet, get_current_user, is_current_user_admin, DevicesViewSet, TagViewSet, SubscriptionsViewSet, UserPreferencesViewSet, LocationsViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UsersViewSet, 'users')
router.register(r'devices', DevicesViewSet, 'devices')
router.register(r'tags', TagViewSet, 'tags')
router.register(r'subscriptions', SubscriptionsViewSet, 'subscriptions')
router.register(r'userpreferences', UserPreferencesViewSet, 'userpreferences')
router.register(r'locations', LocationsViewSet, 'locations')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('get_current_user', get_current_user),
    path('is_admin', is_current_user_admin),
    path('admin/', admin.site.urls)
]

