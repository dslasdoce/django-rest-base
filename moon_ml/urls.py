"""moon_ml URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls import url
from apps.account import views as account
from moon_ml.routers import DefaultRouter
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from moon_ml.jwt import TokenObtainPairView
from django.conf import settings

# viewset routers
router = DefaultRouter()
router.register('profiles', account.ProfileViewSet, basename='profiles')

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),

    # api session authentication
    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),

    # common site urls
    path('api/v1/', include(router.urls)),

    # token authentication
    re_path(r'api/v1/token/?$',
            TokenObtainPairView.as_view(), name='token_obtain_pair'),

    url(r'api/v1/my_profile',
        account.MyProfileViewSet.as_view(
            {'get': 'retrieve', 'patch': 'partial_update'})
        ),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path('django-rq/', include('django_rq.urls'))]
