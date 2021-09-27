"""URL Configuration

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
from core.routers import DefaultRouter
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from core.jwt import TokenObtainPairView
from django.conf import settings
from django.views.generic import TemplateView
from apps.user import views as user
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


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

    # password
    url(r'^api/v1/password/reset/confirm/(?P<token>[-:\w]+)/$',
        user.PasswordResetConfirmView.as_view(),
        name="reset-password-confirm"),
    url(r'^api/v1/password/reset/$',
        user.PasswordResetView.as_view(),
        name="reset-password-request"),
    url(r'^api/v1/password/change/$', user.PasswordChangeView.as_view(),
        name='rest_password_change'),

    # social login redirect oauth2
    path('api/v1/accounts/', include('allauth.urls')),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path('django-rq/', include('django_rq.urls'))]


urlpatterns += [
    path('social-success/',
         TemplateView.as_view(template_name='social_auth/google_login.html')),
]

if settings.DEBUG is True:
    schema_view = get_schema_view(
       openapi.Info(
          title="Snippets API",
          default_version='v1',
          description="Test description",
          terms_of_service="https://www.google.com/policies/terms/",
          contact=openapi.Contact(email="contact@snippets.local"),
          license=openapi.License(name="BSD License"),
       ),
       public=True,
       permission_classes=(permissions.AllowAny,),
    )
    urlpatterns += [
        # swagger docs
        url(r'^docs/api/v1(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^docs/api/v1$', schema_view.with_ui('swagger', cache_timeout=0))
    ]
