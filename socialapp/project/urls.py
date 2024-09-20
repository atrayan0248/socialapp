from __future__ import annotations

from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import authentication
from rest_framework import permissions

# import socialapp.accounts.urls

schema_view = get_schema_view(
    openapi.Info(
        title='Social App API',
        default_version='v1',
        description='API documentation for Social App',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@socialapp.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    authentication_classes=[authentication.TokenAuthentication],
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('socialapp.accounts.urls')),
    path('user/details/', include('socialapp.user_details.urls')),
    # Swagger documentation urls
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
