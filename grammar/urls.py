from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

schema_view = get_schema_view(
   openapi.Info(
      title="Grammar Azi API Documentation",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # Swagger UI endpoints
        # Swagger and ReDoc documentation
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-ui",
    ),
    
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="redoc-ui",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),

    # Core apps
    path('', include('core.urls')),
    path('', include('account.urls')),
    path('', include('blog.urls')),
    path('', include('grammars.urls')),

    # API endpoints with unique prefixes to avoid conflicts
    path('api/', include('grammars.api.urls')),
    path('api/', include('blog.api.urls')),
    path('api/', include('core.api.urls')),
    path('api/', include('account.api.urls')),
)


urlpatterns += [
    # Endpoints for JWT authentication
    path(
        "api/token/", 
        include("users.urls.auth"),
    ),
    path(
        "api/token/refresh/", 
        TokenRefreshView.as_view(), 
        name="token_refresh"
    ),

    path(
        "api/token/verify/", 
        TokenVerifyView.as_view(), 
        name="token_verify"
    ),
    
    # API paths
    path(
        "api/v1/", 
        include("users.urls")
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)